from fastapi import FastAPI, Body
from datetime import datetime
from random import randint


id_length = 6


database = {"id": "BaseModel" # ['login', 'password', 'second_name', 'first_name', 'surname', 'DoB', 'Experience']
             }



app = FastAPI() # uvicorn main:app --reload

@app.get("/")
def hihihaha(data=Body()):
    return f"Main page: {data}"

@app.get("/profile/{id}")
def read_profile(id: int):
    print(database)
    if id in database:
        if (birthdate := database[id].DoB) != None:
            age = datetime.now().year - birthdate.year - (
                    (datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
            return (database[id].model_dump(), f'Возраст = {age}')
    else:
        return "Такого профиля не существует"

@app.post("/profile")
def registration(data=Body()):
    profile = Model(**data)
    while True:
        id = int(''.join([str(randint(0, 9)) for _ in range(id_length)])) # id = случайное {id_length}-значное число
        if id not in database: # и проверяется наличие идентичного id в database
            break

    database[id] = profile
    return {f"Аккаунт создан;  id = {id}; {profile.model_dump()}"}

@app.patch('/profile/{id}')
def patch_profile(id: int, data=Body()):
    if id in database:
        profile = database[id]
        database[id] = profile.model_copy(update=data)
        return 'Профиль был изменён'
    else:
        return "Такого профиля не существует"

@app.put('/profile/{id}')
def patch_profile(id: int, data=Body()):
    if id in database:
        if 'password' in data and 'login' in data:
            database[id] = Model(**data)
            return f'Профиль был изменён'
    else:
        return "Такого профиля не существует"

@app.delete('/profile/{id}')
def patch_profile(id: int, data=Body()):
    if id in database:
        del database[id]
        return "Профиль был удалён"
    else:
        return "Такого профиля не существует"