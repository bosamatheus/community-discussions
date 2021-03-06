"""Comment domain module."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Comment model."""

    comment_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    topic_id: str = Field(default=None, alias="topic")
    reply_comment: str = Field(default=None, alias="reply")
    content: str = Field(...)
    username: str = Field(...)
    discussion_type: str = Field(default="comment", alias="type")
    created: datetime = Field(default_factory=datetime.now)
    updated: Optional[datetime] = Field(default=None)

    class Config:
        """Pydantic config class."""

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": "Sure! I can help you!",
                "username": "Nephew Bob",
                "reply": "54539bf6-7f01-4002-b850-7ec3e9dee441",
            }
        }


class UpdateComment(BaseModel):
    """Comment model for update."""

    content: str = Field(...)
    updated: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        """Pydantic config class."""

        allow_population_by_field_name = True
        schema_extra = {"example": {"content": "Sure! I can help you!"}}
