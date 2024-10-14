#from db_connection import mongodb_client
from datetime import datetime, timedelta
import uuid

class QueryParams:
    def __init__(self, collection, _filter, data=None, _from=None, local_field=None, foreign_field=None, _as=None, project=None):
        self.collection = collection
        self._filter = _filter
        self.data = data
        self._from = _from
        self.local_field = local_field
        self.foreign_field = foreign_field
        self._as = _as
        self.project = project
        

class MongoDBService:
    def __init__(self, db_name = "users"):
        self.db = mongodb_client[db_name]
        self.ids = {}

    async def get_document(self, params):
        return await self.db[params.collection].find_one(params._filter)


    async def set_document(self, params, operator = "set"):
        result = await self.db[params.collection].update_one(
                    params._filter
                    , {
                        f"${operator}": params.data
                    }
                    , upsert = True
                )

        self.ids[params.collection] = result.upserted_id


    async def get_join_documents(self, params):
        pipeline = [
            {"$match": params._filter}
            , {
                "$lookup": {
                    "from": params._from 
                    , "localField": params.local_field 
                    , "foreignField": params.foreign_field 
                    , "as": params._as
                }
            }
            , {
                "$project": params.project
            }
        ]

        return [doc async for doc in self.db[params.collection].aggregate(pipeline)]


def is_token_expired(timestamp, time_dict):
    ts = datetime.fromtimestamp(timestamp)
    token_age = datetime.utcnow() - ts

    return token_age > timedelta(**time_dict)


def get_token():
    return {"token": str(uuid.uuid4()), "created_at": datetime.utcnow().timestamp()}
