from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from PIL import Image
from io import BytesIO

mongo_atlas_url = "mongodb+srv://ibrahim:h0c2YhfienNaTiL1@cluster0.dvytmrt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_atlas_url, 27017)
db = client['gadGradDB']
users = db['Users']


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


def add_history(email, path, res):
    data = convert_image_to_base64(path)

    user = users.find_one({
        'email': email
    })

    history = user.get('history')
    if len(history) > 5:

        history = history[1:]
        history.append(
            {
                "name": path.split('upload/')[1],
                "image_data": data,
                "result": res
            }
        )
        users.update_one(
            {
                "email": email
            },
            {'$set':
                {"history": history}
            }
        )
    else:
        users.update_one(
            {
                "email": email
            },
            {'$push':
                {"history":
                    {
                        "name": path.split('upload/')[1],
                        "image_data": data,
                        "result": res
                    }
                }
            }
        )


def convert_image_to_base64(path):
    with open(path, 'rb') as f:
        image_bytes = f.read()

    base64_bytes = base64.b64encode(image_bytes)
    base64_string = base64_bytes.decode('utf-8')

    return base64_string


def convert_base64_to_image(image_data, name):
    image = base64.b64decode(image_data)
    img = Image.open(BytesIO(image))

    img.save(f'static/history/{name}')
    return f'static/history/{name}'


def get_history(email):
    user = users.find_one({
        "email": email
    })
    history = user.get('history')

    for item in history:
        image_string = item["image_data"]
        path = convert_base64_to_image(image_string, item['name'])
        item["src"] = path


    return history[::-1]
