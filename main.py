from fastapi import FastAPI, Body, HTTPException

from datetime import datetime
from random import randint

from model import Model

database = []

app = FastAPI()  # uvicorn main:app --reload
user_id_length = 6

@app.get("/profile/{user_id}")
def read_profile(user_id: int):
    if len(database):
        for user in database:
            if user.id == user_id:
                if (birthdate := user.DoB) != None:
                    age = datetime.now().year - birthdate.year - (
                            (datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
                    return {**dict(user), 'age': age}
                return {**dict(user), 'age': "null"}
            else:
                raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/profile")
def registration(data=Body()):
    while True:
        user_id = int(''.join([str(randint(0, 9)) for _ in range(user_id_length)]))  # user_id = случайное {user_id_length}-значное число
        for user in database:
            if user.id == user_id:
                break
        break
    profile = Model(**data, id=user_id)
    database.append(profile)
    return profile


@app.patch('/profile/{user_id}')
def patch_profile(user_id: int, data=Body()):
    for i, user in enumerate(database):
        if user.id == user_id:
            database[i].__dict__.update(**data)
            return database[i]
        else:
            raise HTTPException(status_code=404, detail="User not found")


@app.put('/profile/{user_id}')
def put_profile(user_id: int, data=Body()):
    for i, user in enumerate(database):
        if user.id == user_id:
            if 'password' in data and 'login' in data:
                database.remove(user)
                database.append(Model(id=user.id, **data))
                return database[i]
        else:
            raise HTTPException(status_code=404, detail="User not found")


@app.delete('/profile/{user_id}')
def delete_profile(user_id: int):
    for user in database:
        if user.id == user_id:
            database.remove(user)
            return 'User was deleted'
        else:
            raise HTTPException(status_code=404, detail="User not found")
