from pydantic import BaseModel

class TaskSchema(BaseModel):
    task: int