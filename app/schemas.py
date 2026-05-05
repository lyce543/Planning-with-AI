from pydantic import BaseModel

class PlanCreate(BaseModel):
    date: str
    content: str
