from db_connection import mongodb_client
from datetime import datetime, timedelta
import uuid
import asyncio

class MongoDBService:
    def __init__(self, db_name = "users"):
        self.db = mongodb_client[db_name]
        self.ids = {}

    async def get_one_document(self, params: dict):
        return await self.db[params.collection].find_one(params._filter)


    async def set_one_document(self, params: dict, operator = "set"):
        result = await self.db[params.collection].update_one(
                    params._filter
                    , {
                        f"${operator}": params.data
                    }
                    , upsert = True
                )

        self.ids[params.collection] = result.upserted_id


    async def set_list_documents(self, params_list: list):
        tasks = [self.set_one_document(params) for params in params_list]
        tasks = [asyncio.create_task(task) for task in tasks]
        await asyncio.gather(*tasks)


    async def get_join_documents(self, params: dict):
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

        return await self.db[params.collection].aggregate(pipeline)


def is_token_expired(timestamp, time_dict):
    ts = datetime.fromtimestamp(timestamp)
    token_age = datetime.utcnow() - ts

    return token_age > timedelta(**time_dict)


def get_token():
    return {"token": str(uuid.uuid4()), "created_at": datetime.utcnow().timestamp()}
