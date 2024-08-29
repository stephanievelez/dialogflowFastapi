#used to write how an object in a model can be easily mapped using ORM (communication btw programming language and databases).

# build a schema using pydantic
from pydantic import BaseModel

class UserData(BaseModel):
    userId: str
    name: str


    class Config:
        orm_mode = True