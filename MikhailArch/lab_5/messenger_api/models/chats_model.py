from pydantic import BaseModel
from typing import List, Mapping


class ChatModel(BaseModel):
    admins: List[int]
    members: List[int]
    chat_name: str
    messages: List[Mapping]
    is_PtP: bool
