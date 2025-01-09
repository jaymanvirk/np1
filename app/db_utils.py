from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import os
from concurrent.futures import ThreadPoolExecutor
from llm_manager import LLMManager
import asyncio

OLLAMA_URL = os.getenv("OLLAMA_URL")
LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")
EMBED_CHECKPOINT = os.getenv("EMBED_CHECKPOINT")
LLM_INSTRUCTION_GEN = os.getenv("LLM_INSTRUCTION_GEN")
LLMM = LLMManager(OLLAMA_URL, LLM_CHECKPOINT, EMBED_CHECKPOINT, LLM_INSTRUCTION_GEN)


def get_milvus_data(query_embedding, milvus_manager):
    results = milvus_manager.search(query_embedding)
    data = []
    for hits in results:
        for hit in hits:
            data.append(hit.entity.get('data'))

    return data 

def set_milvus_collection():
    connections.connect(
        host=os.getenv("MILVUS_HOST")
        , port=os.getenv("MILVUS_PORT")
    )

    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True)
        , FieldSchema(name="data", dtype=DataType.VARCHAR, max_length=65535)
        , FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=1024)
    ]
    schema = CollectionSchema(fields=fields, description="Data collection")
    collection = Collection(name="data", schema=schema)

    file_path = os.getenv("DATASET_FILE_PATH")

    def insert_batch(batch):
        data = [str(item) for item in batch]
        tasks = [LLMM.get_embedding(item) for item in data]
        embeddings = await asyncio.gather(*tasks)
        collection.insert([{"data": data}, {"embeddings": embeddings}])
    
    def read_csv_batches(file_path, batch_size = 512):
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            while True:
                batch = list(islice(csv_reader, batch_size))
                if not batch:
                    break
                yield batch

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        batches = read_csv_batches(file_path)
        executor.map(insert_batch, batches)

    collection.create_index(
        field_name="embedding"
        , index_params={
            "metric_type": "L2"
            , "index_type": "IVF_FLAT"
        }
    )

    connections.disconnect("default")

    

if __name__ == '__main__':
    set_milvus_collection()

