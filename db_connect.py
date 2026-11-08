"""Connect to existing collections without seeding data or changing indexes.

Database initialization is an explicit administrator task, never API startup.
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient


def db_connect():
    load_dotenv()
    mongo_username = os.getenv("MONGO_USERNAME")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_host = os.getenv("MONGO_HOST")
    # Use the default port unless MONGO_HOST already includes one (e.g. 192.168.0.238:27242)
    if mongo_host and ":" not in mongo_host:
        mongo_host = f"{mongo_host}:27017"
    mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}/?authMechanism=DEFAULT&authSource=footyapp"
    client = MongoClient(mongo_uri)
    db = client['footyapp']
    return db['players'], db['games'], db['tenant']
