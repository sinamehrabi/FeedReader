from sqlalchemy import select

from .init_test import client, test_db, TestingSessionLocal
from src.entities.feed.services import FeedItemsService
from src.entities.feed.models import FeedItem, Feed


def test_feed_creation(test_db):
    response = client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                           "rss_link": "https://realpython.com/atom.xml"})

    assert response.status_code == 201


def test_feed_item_add(test_db):
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})
    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()

    feed_items = db.execute(select(FeedItem)).all()
    assert feed_items is not None


def test_feed_item_add_backoff(test_db):
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xm"})
    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()

    feed = db.execute(select(Feed)).scalar()
    assert feed.updatable is False
    feed.rss_link = "https://realpython.com/atom.xml"
    feed.updatable = True
    db.commit()
    FeedItemsService(db).add_items_to_feeds()
    feed = db.execute(select(Feed)).scalar()
    assert feed.updatable is True

