from typing import List
from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    species: str

    class Config:
        orm_mode = True


class Person(BaseModel):
    name: str
    age: int
    pets: List[Pet]

    class Config:
        orm_mode = True


bones = Pet(name='Bones', species='dog')
orion = Pet(name='Orion', species='cat')
anna = Person(name='Anna', age=20, pets=[bones, orion])

print(anna)
