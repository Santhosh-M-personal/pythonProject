from fastapi import FastAPI, Path, Depends
from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

admins = {}


class Admin(BaseModel):
    user_name: str
    password: str


@app.post('/')
async def create_admin(admin_id: int, admin: Admin):
    if admin_id in admins:
        return "admin already exists"

    admins[admin_id] = admin
    return admins[admin_id]


users = {}


class User(BaseModel):
    name: str
    age: int
    number: int


class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    number: Optional[int] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/get-by-name/{user_id}")
def get_user(*, name: str = Path(None, description="Enter the name of the user to view details")):
    for user_id in users:
        if users[user_id]["Name"] == name:
            return users[user_id]
    return {'Data': 'not found'}


@app.post("/create-user/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users:
        return "user already exists"

    users[user_id] = user
    return users[user_id]


@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id not in users:
        return "user not found"

    if user.name is not None:
        users[user_id].name = user.name

    if user.age is not None:
        users[user_id].age = user.age

    if user.number is not None:
        users[user_id].number = user.number

    return users[user_id]


@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        return "User doesn't exist"

    del users[user_id]
    return "User deleted successfully"
