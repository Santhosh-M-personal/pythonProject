import pymongo
from pymongo import MongoClient
import bcrypt
import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["DeepByte"]
collection = db["Credentials"]


def insert_items(f_name, l_name, user_name, p_no, e_mail, pass_word):
    hashed_pw = bcrypt.hashpw(pass_word.encode('utf-8'), bcrypt.gensalt())
    post1 = {"firstName": f_name, "lastName": l_name, "userName": user_name, "Phone": p_no, "e_Mail": e_mail,
             "password": hashed_pw, "createdTime": datetime.datetime.now().isoformat(),
             "updatedTime": datetime.datetime.now().isoformat()}
    collection.insert_one(post1)
    print("item added")


# insert_items("Santhosh", "M", "sant", 12121, "s.com", '1234')

def update_items(user_name, e_mail):
    myquery = {
             "userName": user_name,
             }
    my_value = {"$set": {
        "e_Mail": e_mail,
        "updatedTime": datetime.datetime.now().isoformat()
    }}
    collection.update_one(myquery, my_value)
    print("item added")


def check_password(userID, password):
    username_from_DB = collection.find_one({"userName": userID})
    # print("username_from_DB>>> ", username_from_DB)
    if username_from_DB["userName"] == userID:
        password1 = bytes(password, 'utf-8')
        # print("password1>>> ", password1)
        if bcrypt.checkpw(password1, username_from_DB["password"]):
            print('Login success!\n')
        else:
            print("Incorrect password")
    else:
        print("Incorrect User ID")

    #     if password == hash_pw:
    #         print('Login success!\n')
    #     else:
    #         print("Incorrect password")
    # else:
    #     print("Incorrect User ID")


while True:
    print("\n OPERATIONS AVAILABLE \n")
    print("1. Insert\n")
    print("2. Update\n")
    print("3. Delete\n")
    print("4. Check Login\n")
    print("5. Display the Records\n")
    print("6. Display the Record of Particular User\n")
    print("7. Quit\n")
    option = input("\n Please Select The Operation To be Performed: \n")
    if option == "1":

        user_name = input("Enter User Name \n")
        username_from_DB = collection.find_one({"userName": user_name})
        pass_word, f_name, l_name, p_no, e_mail = " ", " ", " ", " ", ""
        if username_from_DB["userName"] != user_name:
            pass_word = input("Enter password \n")
            f_name = input("Enter First Name \n")
            l_name = input("Enter Last Name \n")
            p_no = input("Enter Phone Number \n")
            e_mail = input("Enter email id \n")

        else:
            print("Username Already Exists")

        insert_items(user_name, pass_word, f_name, l_name, p_no, e_mail)

    elif option == "2":
        user_name = input("Enter User Name of whose email id has to be updated: \n")
        e_mail = input("Enter email id \n")
        update_items(user_name, e_mail)

    elif option == "3":
        user_name = input("Enter User Name  to be deleted: \n")
        myquery = {"userName": user_name}
        collection.delete_one(myquery)

    elif option == "4":
        userID = input('Enter User ID > ')
        password = input('Enter Password > ')
        check_password(userID, password)

    elif option == "5":
        document = collection.find({})
        for file in document:
            print(file)

    elif option == "6":
        userID = input('Enter User ID > ')
        cursor = collection.find_one({"userName": userID})
        print(cursor)

    elif option == "7":
        exit(0)

    else:
        print("Choose the correct option")

        break
