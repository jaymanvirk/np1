from models import MongoDBService, get_token


class UserManagement(MongoDBService):
    def __init__(self, db_name = "users"):
        super().__init__(db_name)
        self.collections = {"profiles": self.db["profiles"]
                            , "auths": self.db["auths"]
                            , "sessions": self.db["sessions"]
                            }

    def set_user_id(self, user_id):
        self.user_id = user_id


    async def get_insert_user_id(self, email: str):
        email_dict = {"email": email}
        user_profile = await self.collections["profiles"].find_one(email_dict)

        if not user_profile:
            result = await self.collections["profiles"].insert_one(email_dict)
            user_profile = {}
            user_profile["_id"] = result.inserted_id
            await self.collections["auths"].insert_one({"user_id": user_profile["_id"]})

        self.set_user_id(user_profile["_id"])

        return user_profile["_id"]


    async def get_update_auth_token(self, operator = "set"):
        auth_dict = get_token()

        await self.collections["auths"].update_one(
            {"user_id": self.user_id}
            , {
                f"${operator}": auth_dict
            }
        )

        return auth_dict["token"]


    async def set_user_session(self, data: dict) -> None:
        user_id_dict = {"user_id": self.user_id}
        user_session = await self.collections["sessions"].find_one(user_id_dict)

        if not user_session:
            await self.collections["sessions"].insert_one({**user_id_dict, **data})
        else:
            await self.collections["sessions"].update_one(
                user_id_dict
                , {"$set": data}
            )





