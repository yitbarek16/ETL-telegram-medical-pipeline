from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    object_class: str
    mention_count: int

from datetime import date

class ChannelActivity(BaseModel):
    date: date
    message_count: int


class Message(BaseModel):
    message_id: int
    message_length: Optional[int]
    message_text: Optional[str]
