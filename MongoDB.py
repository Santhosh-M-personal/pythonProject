from pymongo import MongoClient
from cryptography.fernet import Fernet

client = MongoClient("mongodb://localhost:27017/")
db = client["DeepByte"]
collection = db["Employee"]
collection2 = db["Credentials"]


def add_items():
    post1 = {"Name": "Santhosh", "Role": "PD"}

    x = collection.insert_one(post1)
    return "items entered into db"


# print(add_items())


def find_db(value):
    result = collection.find_one({"Name": value})
    print(result)


value = "Santhosh"
(find_db(value))


def find_all_db():
    result = collection.find()
    for x in result:
        print(x)


# (find_all_db())


def update_db():
    myQuery = {"Name": "Sharath"}
    NewValues = {"$set": {"Name": "SharathDB"}}

    collection.update_one(myQuery, NewValues)

    # print after the update:
    for x in collection.find({"Name": "Sharath DB"}):
        print(x)


# update_db()


def delete_db():
    myQuery = {"Name": "Vinay B V"}

    x = collection.delete_many(myQuery)
    print(x.deleted_count, "Elements deleted")


# delete_db()


def credentials(name, password):
    msg = password
    key = Fernet.generate_key()
    fernet = Fernet(key)
    enc_msg = fernet.encrypt(msg.encode())
    print(enc_msg)
    post = {"User Name": name, "Password": enc_msg}
    collection2.insert_one(post)
    dec_msg = fernet.decrypt(enc_msg).decode()
    print(dec_msg)


# credentials("Santhosh", "1234")
