import requests
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import numpy as np
mongo_atlas_url = "mongodb+srv://ibrahim:h0c2YhfienNaTiL1@cluster0.dvytmrt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_atlas_url, 27017)
db = client['gadGradDB']
users = db['Users']


# user = users.find_one({
#     "email": "ibrahim@gmail.com"
# })
#
#
# history = user.get('history')
#
# for key in history:
#     print(key)
#     key = np.array(list(key))
#     image = Image.fromarray(key)
#     image.show()
#




def register_user(fname, lname, email, password, gender):
    new_user = {
        "name": f"{fname} {lname}",
        "password": generate_password_hash(password),
        "email": email,
        "gender": gender,
        "history": {}
    }
    users.insert_one(new_user)

    return email


def login_user(email, password):
    user = users.find_one({
        "email": email
    })

    if check_password_hash(password=password, pwhash=user['password']):
        print("Logged in successfully")


def add_history(email, array, result):
    users.update_one(
        {
            "email": email
        },
        {'$set':
            {'history': {
                str(array): result
            }}
        }
    )
