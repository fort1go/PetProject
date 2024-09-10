from fastapi import FastAPI, Body, HTTPException

from datetime import datetime

from model import Model

database = []

app = FastAPI()  # uvicorn main:app --reload

@app.get("/profile/{user_id}")
def read_profile(user_id: str):
    for user in database:
        if user.id == user_id:
            if (birthdate := user.DoB) != None and user.age != None:
                user.age=datetime.now().year - birthdate.year - (
                        (datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/profile")
def registration(data: Model = Body()):
    database.append(data)
    return data


@app.patch('/profile/{user_id}')#Забить.Будет разбираться фронт
def patch_profile(user_id: str, data: Model=Body()):
    for i, user in enumerate(database):
        if user.id == user_id:
            database[i] = data
            return database[i]
    raise HTTPException(status_code=404, detail="User not found")


@app.put('/profile/{user_id}')
def put_profile(user_id: str, data: Model = Body()):
    for user in database:
        if user.id == user_id:
            database.remove(user)
            data.id = user_id
            database.append(data)
            return database[-1]
    raise HTTPException(status_code=404, detail="User not found")

@app.delete('/profile/{user_id}')
def delete_profile(user_id: str):
    for user in database:
        if user.id == user_id:
            database.remove(user)
            return 'User was deleted'
    raise HTTPException(status_code=404, detail="User not found")