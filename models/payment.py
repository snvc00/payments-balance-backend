from datetime import datetime
from typing import Optional
from uuid import uuid1
from pydantic import BaseModel

from models.owner import Owner

class Payment(BaseModel):
    id: str = str(uuid1())
    title: str
    description: Optional[str] = None
    date: datetime = datetime.now().date()
    tags: Optional[list] = []
    owner: Owner
    cost: float
    contribution: float

    def to_json(self):
        self.date = str(self.date)
        return self.dict()
