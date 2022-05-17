from database.connection import start_connection
from models.user import User

class UserDB:
    def __init__(self) -> None:
        collection_name = "user"
        self.collection = start_connection(collection_name)

    async def create_user(self,data):
        document = data
        result = await self.collection.insert_one(document)
        return document
    
    async def find_user(self,username:str):
        result = await self.collection.find_one({"username":username})
        return result
    
    async def get_users(self):
        users = []

        cursor = self.collection.find({})

        async for document in cursor:

            users.append(User(**document))

        return users