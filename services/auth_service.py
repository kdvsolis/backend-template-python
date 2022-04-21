import pymongo
import jwt
import os
from flask import jsonify, request
from datetime import datetime, timedelta
from functools import wraps
from passlib.context import CryptContext

client = pymongo.MongoClient(os.environ.get('MONGO_CLIENT', ''))
db = client["sloovi"]
auth_collection = db["user"]
secret_key = os.environ.get('SECRET_KEY', '')

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'authorization' in request.headers:
           token = request.headers['authorization']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token.replace("Bearer ",""), secret_key, algorithms=["HS256"])
           current_user = auth_collection.find_one({"email": data["email"]})
       except Exception as e:
           print(e)
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator

class AuthService:
    def __init__(self):
        """"""

    def register(self, body):
        user = auth_collection.find_one({"email": body["email"]})
        if(user != None):
            return {
                "success": False,
                "message": "User exist"
            }
        body["password"] = pwd_context.encrypt(body["password"])
        auth_collection.insert_one(body)
        return {
            "success": True
        }

    def login(self, email, password):
        user = auth_collection.find_one({"email": email})
        if(user != None and pwd_context.verify(password, user['password'])):
            return {
                "success": True,
                "token": jwt.encode({'email' : email, 'exp' : datetime.utcnow() + timedelta(minutes=45)}, secret_key, "HS256")
            }
        return {
            "success": False
        }