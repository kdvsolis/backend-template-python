import os, sys
sys.path.insert(0, os.path.abspath("../"))

import pymongo
from bson import ObjectId
from bson.json_util import dumps, loads
from datetime import datetime, timedelta

client = pymongo.MongoClient(os.environ.get('MONGO_CLIENT', ''))
db = client["sloovi"]
template_collection = db["template"]
secret_key = os.environ.get('SECRET_KEY', '')

class TemplateService:
    def __init__(self):
        """"""
    def templateSingle(self, id):
        data = loads(dumps(template_collection.find_one({"_id": ObjectId(id)})))
        if(data != None):
            print(data)
            data['_id'] = str(data['_id'])
            return {
                "success": True,
                "data": data
            }
        return {
                "success": False
            }
    def templateAll(self):
        data = loads(dumps(template_collection.find()))
        if(data != None):
            for i in range(len(data)):
                data[i]['_id'] = str(data[i]['_id'])
            return {
                "success": True,
                "data": data
            }
        return {
                "success": False
            }
    def templateNew(self, body):
        try:
            id = str(template_collection.insert_one(body).inserted_id)
            return {
                "success": True,
                "id": id
            }
        except Exception as e:
            return {
                "success": False
            }

    def templateUpdate(self, id, body):
        data = template_collection.find_one({"_id": ObjectId(id)})
        if(data != None):
            template_collection.update_one({"_id": ObjectId(id)}, {"$set": body})
            print(data)
            return {
                "success": True,
                "data": body
            }
        return {
                "success": False
            }

    def templateDelete(self, id):
        data = template_collection.find_one({"_id": ObjectId(id)})
        if(data != None):
            template_collection.delete_one({"_id": ObjectId(id)})
            return {
                "success": True,
                "id": id
            }
        return {
                "success": False
            }