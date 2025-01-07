from pymilvus import Collection, connections
import os

class MilvusManager:
    def __init__(self
                 , host=os.getenv("MILVUS_HOST")
                 , port=os.getenv("MILVUS_PORT")
                 , collection_name=os.getenv("MILVUS_COLLECTION_NAME")
                 ):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.collection = None

    def connect(self):
        connections.connect(host=self.host, port=self.port)
        self.collection = Collection(self.collection_name)
        self.collection.load()

    def disconnect(self):
        if self.collection:
            self.collection.release()
        connections.disconnect()

    def search(self, query_embedding, limit=3):
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embeddings",
            limit=limit,
            output_fields=["data"] 
        )

        return results
