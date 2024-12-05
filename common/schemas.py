from typing import Optional

from pydantic import BaseModel


class ConversationDto(BaseModel):
    id: Optional[int]
    message: str

    class Config:
        from_attributes = True
