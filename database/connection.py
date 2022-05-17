import motor.motor_asyncio
from decouple import config
import certifi

def start_connection(collection_name:str):
    # CONNECTION_URL = "mongodb+srv://tronajay:3g3qke8XIS2fVYMA@cluster1.osquw.mongodb.net/?retryWrites=true&w=majority"
    CONNECTION_URL = config("MONGODB_CONN_URL")
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_URL,tlsCAFile=certifi.where())
    db = client.tododb
    if collection_name == "todo":
        collection = db.todo
    else:
        collection = db.user
    return collection