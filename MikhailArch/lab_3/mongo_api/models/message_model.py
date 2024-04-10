from pydantic import BaseModel
from typing import List, Mapping
from datetime import datetime


class Message(BaseModel):
    message_text: str
    send_date: datetime
    member: int
