from sqlalchemy.orm import relationship
from src.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Boolean

from ...utils import get_current_datetime


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    link = Column(String, nullable=True)
    rss_link = Column(String, unique=True, index=True)
    last_updated = Column(DateTime, nullable=True)
    updatable = Column(Boolean, nullable=False, default=True)
    feed_items = relationship("FeedItem")
    user_feeds = relationship("UserFeed")
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)
    deleted_at = Column(DateTime, nullable=True)


class FeedItem(Base):
    __tablename__ = "feeds_items"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(ForeignKey(Feed.id), index=True)
    title = Column(String(200))
    link = Column(String)
    updated_feed_item = Column(DateTime)
    summary = Column(String)
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)
    deleted_at = Column(DateTime, nullable=True)


class UserFeed(Base):
    __tablename__ = "user_feeds"
    __table_args__ = (UniqueConstraint('user_id', 'feed_id', name='_user_feed_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), index=True)
    feed_id = Column(ForeignKey(Feed.id))
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)
    deleted_at = Column(DateTime, nullable=True)


class UserFeedItemsRead(Base):
    __tablename__ = "user_feed_items_read"
    __table_args__ = (UniqueConstraint('user_id', 'feed_item_id', name='_user_feed_items_read_uc'),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), index=True)
    feed_item_id = Column(ForeignKey(FeedItem.id))
    feed_id = Column(ForeignKey(Feed.id))
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)


class UserFeedItemsFavorite(Base):
    __tablename__ = "user_feed_items_favorite"
    __table_args__ = (UniqueConstraint('user_id', 'feed_item_id', name='_user_feed_items_favorite_uc'),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), index=True)
    feed_item_id = Column(ForeignKey(FeedItem.id))
    feed_id = Column(ForeignKey(Feed.id))
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)


class UserFeedItemsComment(Base):
    __tablename__ = "user_feed_items_comment"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), index=True)
    feed_item_id = Column(ForeignKey(FeedItem.id))
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)
