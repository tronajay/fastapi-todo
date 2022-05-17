from pydantic import BaseModel, Field

class Todo(BaseModel):

    name: str = Field(...)
    description: str = Field(...)