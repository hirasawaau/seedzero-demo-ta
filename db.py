from beanie import Document

class Profile(Document):
    name: str
    surname: str
    age: int | None = None