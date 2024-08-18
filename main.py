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
                if (birthdate := user.DoB) != None and user.age != None:
                    user.__dict__.update(age=datetime.now().year - birthdate.year - (
                            (datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day)))
                return user
            else:
                raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/profile")
def registration(data: Model = Body()):
    while True:
        user_id = int(''.join([str(randint(0, 9)) for _ in range(user_id_length)]))  # user_id = случайное {user_id_length}-значное число
        for user in database:
            if user.id == user_id:
                break
        break
    data.__dict__.update(id=user_id)
    profile = data
    database.append(profile)
    return profile


@app.patch('/profile/{user_id}')
def patch_profile(user_id: int, data: Model=Body()):
    for i, user in enumerate(database):
        if user.id == user_id:
            database[i] = data.model_copy()
            return database[i]
        else:
            raise HTTPException(status_code=404, detail="User not found")


@app.put('/profile/{user_id}')
def put_profile(user_id: int, data: Model = Body()):
    for user in database:
        print(user.id == user_id)
        if user.id == user_id:
            if 'password' in dict(data) and 'login' in dict(data):
                database.remove(user)
                profile = data
                data.__dict__.update(id=user_id)
                database.append(profile)
                return database[-1]
            else:
                raise HTTPException(status_code=404, detail="Password or Login not found")
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