from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime
from random import randint


id_length = 6


class Model(BaseModel):
    login: str = 'aa'
    password: str = 'aa'
    second_name: str = 'second_name'
    first_name: str = 'first_name'
    surname: str = 'surname'
    DoB: datetime = datetime(2024,1,1)
    Expirience: float = 0


database = {"id": "BaseModel" # ['login', 'password', 'second_name', 'first_name', 'surname', 'DoB', 'Experience']
             }



app = FastAPI() # uvicorn main:app --reload

@app.get("/")
def hihihaha(data=Body()):
    return f"Main page: {data}"

@app.get("/profile/{id}")
def read_profile(id: int, data=Body()):
    if id in database:
        if data["password"] == database[id].password and data["login"] == database[id].login:
            birthdate = database[id].DoB
            age = datetime.now().year - birthdate.year - ((datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
            return (database[id].model_dump(), f'Возраст = {age}')
        else:
            return "Неправильный логин или пароль"
    else:
        return "Такого профиля не существует"

@app.post("/profile")
def registration(data=Body()):
    profile = Model(password=data["password"], login=data["login"])
    while True:
        id = int(''.join([str(randint(0, 9)) for _ in range(id_length)])) # id = случайное {id_length}-значное число
        if id not in database: # и проверяется наличие идентичного id в database
            break

    database[id] = profile
    return {f"Аккаунт создан;  id = {id}; {profile.model_dump()}"}