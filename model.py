from pydantic import BaseModel, validator
from datetime import datetime


class Model(BaseModel):
    id: int = 0
    login: str
    password: str
    second_name: str = None # 'second_name'
    first_name: str = None # 'first_name'
    surname: str = None # 'surname'
    DoB: datetime = None # datetime(2020,1,1)
    expirience: float = None # 0
    age: int = None

    # @validator("DoB")
    # @classmethod
    # def validate_date_of_birth(cls, v):
    #     if v and v >= datetime.today():
    #         return 'Дата рождения должна быть в прошлом'
    #     return v