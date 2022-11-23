from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class CreateFeedDTO(BaseModel):
    title: str
    link: str = None
    rss_link: str


class FeedInfoDTO(CreateFeedDTO):
    id: int
    last_updated: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserFeedInfoDTO(CreateFeedDTO):
    id: int
    last_updated: Optional[datetime]


class FeedItemDTO(BaseModel):
    id: int = None
    title: str = None
    link: str = None
    updated_feed_item: Optional[Union[str, datetime]] = None
    summary: str = None
    created_at: datetime = None
    is_read: bool = None
    is_liked: bool = None


class SelectFeedDTO(BaseModel):
    is_selected: bool


class UnreadCountFeedItemsDTO(BaseModel):
    unread_count: int


class CreateCommentDTO(BaseModel):
    text: str


class ReadCommentsDTO(BaseModel):
    id: int
    text: str
    created_at: datetime
