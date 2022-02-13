from typing import Optional
from pydantic import BaseModel


class Owner(BaseModel):
    fullname: str
    email: Optional[str]
