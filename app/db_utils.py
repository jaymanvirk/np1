from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import os
import pandas as pd

connections.connect(os.getenv("MILVUS_CON_NAME"), host=os.getenv("MILVUS_HOST"), port=os.getenv("MILVUS_PORT"))

embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=4096)
schema = CollectionSchema(fields=[embedding_field], description="Collection with embeddings only")
collection = Collection(name="data", schema=schema)
data = pd.read_csv(os.getenv("DATASET_FILE_PATH"))
batch_size = 512
ln = len(data)
for start in range(0, ln, batch_size): 
    end = min(start + batch_size, ln)
    batch = data.iloc[start:end]
    #TODO: run parallel embedding generation
    collection.insert([embeddings])

collection.create_index(field_name="embedding", index_params={
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
})

