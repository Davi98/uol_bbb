from pymongo import MongoClient, ALL
from log import log
import datetime

class Mongo:


    def __init__(self,uri):
        database = "uol"
        collection = "bbb"
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]


    def save(self,document):
        if document is None:
            return None
        try:
            result = self.collection.insert_one(document)
            log().info(f"{__name__}: Document inserted _id: {result.inserted_id}")
            return {'_id': result.inserted_id, **document}

        except Exception as err:
            log().error(f"{__name__}: Error in save method: {type(err)} => {err}")