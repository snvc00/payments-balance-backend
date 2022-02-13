from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.owner import Owner


class Payment(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    date: datetime = datetime.now().date()
    tags: Optional[list] = []
    owner: Owner
    cost: float
    contribution: float
