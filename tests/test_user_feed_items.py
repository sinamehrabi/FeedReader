from sqlalchemy import select

from src.entities.feed import UserFeedItemsRead, UserFeedItemsFavorite, UserFeedItemsComment
from src.entities.feed.services import FeedItemsService
from .init_test import client, test_db, TestingSessionLocal


def test_user_feed_item_read_action(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})

    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()
    client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    response = client.post("/users/me/feeds/1/items/1/read",
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_read = db.execute(
        select(UserFeedItemsRead).where(UserFeedItemsRead.user_id == 1, UserFeedItemsRead.feed_id == 1,
                                        UserFeedItemsRead.feed_item_id == 1)).scalar()
    assert user_feed_item_read is not None


def test_user_feed_item_unread_action(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})

    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()
    client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    response = client.post("/users/me/feeds/1/items/1/read",
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_read = db.execute(
        select(UserFeedItemsRead).where(UserFeedItemsRead.user_id == 1, UserFeedItemsRead.feed_id == 1,
                                        UserFeedItemsRead.feed_item_id == 1)).scalar()
    assert user_feed_item_read is not None

    response = client.delete("/users/me/feeds/1/items/1/unread",
                             headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_read = db.execute(
        select(UserFeedItemsRead).where(UserFeedItemsRead.user_id == 1, UserFeedItemsRead.feed_id == 1,
                                        UserFeedItemsRead.feed_item_id == 1)).scalar()
    assert user_feed_item_read is None


def test_user_feed_item_like_action(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})

    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()
    client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    response = client.post("/users/me/feeds/1/items/1/like",
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_liked = db.execute(
        select(UserFeedItemsFavorite).where(UserFeedItemsFavorite.user_id == 1, UserFeedItemsFavorite.feed_id == 1,
                                            UserFeedItemsFavorite.feed_item_id == 1)).scalar()
    assert user_feed_item_liked is not None


def test_user_feed_item_dislike_action(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})

    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()
    client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    response = client.post("/users/me/feeds/1/items/1/like",
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_liked = db.execute(
        select(UserFeedItemsFavorite).where(UserFeedItemsFavorite.user_id == 1, UserFeedItemsFavorite.feed_id == 1,
                                            UserFeedItemsFavorite.feed_item_id == 1)).scalar()
    assert user_feed_item_liked is not None

    response = client.delete("/users/me/feeds/1/items/1/dislike",
                             headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_liked = db.execute(
        select(UserFeedItemsFavorite).where(UserFeedItemsFavorite.user_id == 1, UserFeedItemsFavorite.feed_id == 1,
                                            UserFeedItemsFavorite.feed_item_id == 1)).scalar()
    assert user_feed_item_liked is None


def test_get_user_feed_items(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})

    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()
    client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    client.post("/users/me/feeds/1/items/1/read",
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    client.post("/users/me/feeds/1/items/2/read",
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    client.post("/users/me/feeds/1/items/4/like",
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    response = client.get("/users/me/feeds/1/items",
                          headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 200

    for item in response.json().get("items"):
        if item.get("id") == 1 or item.get("id") == 2:
            assert item.get("is_read") is True
        else:
            assert item.get("is_read") is False

        if item.get("id") == 4:
            assert item.get("is_liked") is True
        else:
            assert item.get("is_liked") is False


def test_user_feed_item_comment(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})

    db = TestingSessionLocal()
    FeedItemsService(db).add_items_to_feeds()
    client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    response = client.post("/users/me/feeds/1/items/1/comments", json={"text": "test1"},
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    response = client.post("/users/me/feeds/1/items/1/comments", json={"text": "test2"},
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})

    assert response.status_code == 204

    user_feed_item_comments = db.execute(
        select(UserFeedItemsComment).where(UserFeedItemsComment.user_id == 1,
                                           UserFeedItemsComment.feed_item_id == 1)).scalars().all()
    assert user_feed_item_comments is not None
    assert len(user_feed_item_comments) == 2





