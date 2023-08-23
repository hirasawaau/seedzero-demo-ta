from pydantic import BaseModel

class ProfileBody(BaseModel):
    name: str
    surname: str
    age: int | None = None