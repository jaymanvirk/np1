from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from llm_manager import LLMManager

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

    data = pd.read_csv(os.getenv("DATASET_FILE_PATH"))

    batch_size = 512
    ln = len(data)
    num_batches = ln // batch_size + (ln % batch_size != 0)*1
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        batches = [data.iloc[i*batch_size:(i+1)*batch_size] for i in range(num_batches)]
        list(executor.map(insert_batch, batches))

    collection.create_index(
        field_name="embedding"
        , index_params={
            "metric_type": "L2"
            , "index_type": "IVF_FLAT"
        }
    )

    connections.disconnect("default")


def insert_batch(batch):
    texts = batch['data'].tolist()
    embeddings = [LLMM.get_embedding(text) for text in texts]
    collection.insert([texts, embeddings])
    

if __name__ == '__main__':
    set_milvus_collection()

