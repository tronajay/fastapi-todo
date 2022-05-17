from database.connection import start_connection
from models.todo import Todo

class TodoDB:
    def __init__(self) -> None:
        collection_name = "todo"
        self.collection = start_connection(collection_name)

    async def todo_list(self):

        todos = []

        cursor = self.collection.find({})

        async for document in cursor:

            todos.append(Todo(**document))

        return todos

    async def create_new_todo(self,todo):
        document = todo
        result = await self.collection.insert_one(document)
        document.pop("_id")
        return document



    async def get_todo_detail(self,name):

        document = await self.collection.find_one({"name": name})
        document.pop("_id")
        return document



    async def update_todo(self,name,data):

        await self.collection.update_one({"name": name}, { "$set": { 'name': data["name"],'desc':data["desc"] } })

        document = await self.collection.find_one({"name": data["name"]})
        document.pop("_id")
        return document



    async def delete_todo(self,name):

        await self.collection.delete_one({"name": name})

        return True

