import pymongo as pymongo
from pymongo.server_api import ServerApi
from fastapi.encoders import jsonable_encoder
from backend.models import *

client = pymongo.MongoClient("mongodb+srv://shesha4572:ivH18IXrTuzh8Hrh@cluster0.evucoe3.mongodb.net/?retryWrites=true&w=majority" , server_api=ServerApi('1'))
db = client.Voting_DAPP
col = db.voters

#first name
#lastname
#dob
#aadhaar
#email
#wallet id
#password hashed
#eligibility for voting

def checkAadhaarUsed(aadhaar : int):
    query = {"aadhaar"  : aadhaar}
    res = list(col.find(query))
    if len(res) == 0:
        return False
    return True

def create_user_db(user : UserForm):
    col.insert_one(jsonable_encoder(user))

def get_user_details(aadhaar : int):
    query = {"aadhaar": aadhaar}
    res = list(col.find(query))
    return UserForm(**res[0])
