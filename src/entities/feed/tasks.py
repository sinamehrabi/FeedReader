import logging
from .services import FeedItemsService
from celery import shared_task
from ...database import SessionLocal


@shared_task
def add_feed_items():
    db = SessionLocal()
    logging.info("add to feed started")
    FeedItemsService(db).add_items_to_feeds()
    logging.info("add to feed stoped")
