from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from random import randint


class Model(BaseModel):
    login: str
    password: str
    second_name: str = 'second_name'
    first_name: str = 'first_name'
    surname: str = 'surname'
    DoB: datetime = datetime("2024-01-01")
    Expirience: float = 0


database = {"id": "BaseModel" # ['login', 'password', 'second_name', 'first_name', 'surname', 'DoB', 'Experience']
             }



app = FastAPI()

@app.get("/profile/{profile_id}")
def read_profile(profile_id: int, password: str, login: str):
    if profile_id in database:
        if password == database[id].password and login == database[id].login:
            birthdate = database[id].DoB
            age = datetime.now().year - birthdate.year - ((datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
            return {database[id].model_dump(), f'Возраст = {age}'}
        else:
            return "Неправильный логин или пароль"
    else:
        return "Такого профиля не существует"

@app.post("/profile")
def registration(profile: Model, password: str, login: str):
    while True:
        id = int(''.join([str(randint(0, 9)) for _ in range(6)])) # id = случайное шестизначное число
        if id not in database: # и проверяется наличие идентичного id в database
            break

    database[id] = profile()
    return {f"Аккаунт создан\n"
            f"id = {id}\n"
            f"{profile.model_dump()}"
            }