from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6)
    age: int | None= Field(gt=0, le=150,default=None)
    email: str = Field(min_length=6, max_length=20)

class UserUpdate(BaseModel):
    username: str | None = Field(min_length=3, max_length=20,default=None)
    password: str | None = Field(min_length=6,default=None)
    age: int | None = Field(gt=0, le=150,default=None)
    email: str | None = Field(min_length=6, max_length=20,default=None)

class UserOut(BaseModel):
    id: int
    username: str