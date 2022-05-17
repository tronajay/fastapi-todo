from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)