from models import MongoDBService, get_token


class UserManagement(MongoDBService):
    def __init__(self, db_name = "users"):
        super().__init__(db_name)
        self.collections = {"profiles": self.db["profiles"]
                            , "auths": self.db["auths"]
                            , "sessions": self.db["sessions"]
                            }
        self.ids = {}


    async def get_one_document(self, collection_name: str, _filter):
        return await self.collections[collection_name].find_one(_filter)


    async def set_one_document(self, data: dict, collection_name: str, _filter, operator = "set"):
        collection = self.collections[collection_name]

        result = await self.get_one_document(collection_name = collection_name
                                                    , _filter = _filter)
        if not result:
            tmp = await collection.insert_one(data)
            result = {}
            result["_id"] = tmp.inserted_id
        else:
            await collection.update_one(
                _filter
                , {
                    f"${operator}": data
                }
            )

        self.ids[collection_name] = result["_id"]


    async def set_user_profile(self, data: dict):
        await self.set_one_document(data = data
                            , collection_name = "profiles"
                            , _filter = {"email": data["email"]}
                            )

    async def set_user_auth(self, data: dict):
        await self.set_one_document(data = data
                            , collection_name = "auths"
                            , _filter = {"token": data["token"]}
                            )

    def set_user_sign_in(self, data: dict):
        args = [{}]

        [await self.set_one_document(d) for d in args]


    async def set_user_session(self, data: dict) -> None:
        collection_name = "sessions"
        collection = self.collections[collection_name]
        _filter = {"token": data["token"]}

        user_session = await self.get_one_document(collection_name = collection_name
                                                    , _filter = _filter)
        if not user_session:
            await collection.insert_one(data)
        else:
            await collection.update_one(
                _filter
                , {"$set": data}
            )


    async def get_user_profile(self, session_token):
        collection_name = "sessions"
        collection = self.collections["sessions"]

        pipeline = [
            {"$match": {"token": session_token}}
            , {
                "$lookup": {
                    "from": "profiles"
                    , "localField": "user_id"
                    , "foreignField": "_id"
                    , "as": "user_profile"
                }
            }
            , {
                "$project": {
                    "_id": 0
                }
            }
        ]

        user_profile = await collection.aggregate(pipeline)

        return user_profile





