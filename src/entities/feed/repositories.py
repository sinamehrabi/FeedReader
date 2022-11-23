from sqlalchemy import select, exists, update, case, func
from fastapi_pagination.ext.sqlalchemy_future import paginate
from .models import Feed, FeedItem, UserFeed, UserFeedItemsRead, UserFeedItemsFavorite, UserFeedItemsComment


class FeedItemRepository:
    def __init__(self, db_session):
        self.db = db_session
        self.feed_items = []

    def add_feed_item(self, feed_id, feed_item, feed_item_last_published):
        self.feed_items.append(FeedItem(
            feed_id=feed_id,
            title=feed_item.title,
            link=feed_item.link,
            updated_feed_item=feed_item_last_published,
            summary=feed_item.summary
        ))

    def feed_item_bulk_insert(self):
        self.db.bulk_save_objects(self.feed_items)
        self.db.commit()
        self.feed_items = []


class FeedRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_all_feeds(self):
        feeds = select(Feed.id, Feed.title, Feed.link, Feed.rss_link, Feed.last_updated, Feed.created_at,
                       Feed.updated_at).where(Feed.deleted_at.is_(None))
        return paginate(self.db, feeds)

    def get_all_updatable_feeds(self):
        return self.db.execute(select(Feed).where(Feed.updatable.is_(True))).scalars().all()

    def get_feed_exist(self, rss_link):
        query = select(Feed).where(Feed.rss_link == rss_link)
        is_exist = self.db.execute(
            exists(query).select()).scalar_one()
        return is_exist

    def create_feed(self, feed_data):
        feed_obj = Feed(
            title=feed_data.title,
            link=feed_data.link,
            rss_link=feed_data.rss_link,
        )
        self.db.add(feed_obj)
        self.db.commit()

    def update_feed(self, feed_id, update_fields):
        values_for_update = {}
        for key, value in update_fields.items():
            values_for_update[getattr(Feed, key)] = value
        self.db.execute(update(Feed).where(Feed.id == feed_id).values(values_for_update))
        self.db.commit()


class UserFeedRepository:

    def __init__(self, db_session):
        self.db = db_session

    def user_feed_exists(self, user_id, feed_id):
        query = select(UserFeed).where(UserFeed.feed_id == feed_id, UserFeed.user_id == user_id)
        is_exist = self.db.execute(
            exists(query).select()).scalar_one()
        return is_exist

    def select_feed_by_user(self, user_id, feed_id):
        self.db.add(UserFeed(
            user_id=user_id,
            feed_id=feed_id
        ))
        self.db.commit()

    def deselect_feed_by_user(self, user_id, feed_id):
        user_feed = self.db.execute(
            select(UserFeed).where(UserFeed.feed_id == feed_id, UserFeed.user_id == user_id)).scalar()

        self.db.delete(user_feed)
        self.db.commit()

    def read_all_user_feeds(self, user_id):
        user_feeds = select(UserFeed, Feed.id, Feed.title, Feed.link, Feed.rss_link, Feed.last_updated).join(
            Feed).where(UserFeed.user_id == user_id)
        return paginate(self.db, user_feeds)


class UserFeedItemsRepository:

    def __init__(self, db_session):
        self.db = db_session

    def user_feed_item_read_exists(self, user_id, feed_id, feed_item_id):
        query = select(UserFeedItemsRead).where(UserFeedItemsRead.feed_item_id == feed_item_id,
                                                UserFeedItemsRead.user_id == user_id,
                                                UserFeedItemsRead.feed_id == feed_id)
        is_exist = self.db.execute(
            exists(query).select()).scalar_one()
        return is_exist

    def read_action(self, user_id, feed_id, feed_item_id):
        user_feed_item = UserFeedItemsRead(user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id)
        self.db.add(user_feed_item)
        self.db.commit()

    def unread_action(self, user_id, feed_id, feed_item_id):
        user_feed_item = self.db.execute(select(UserFeedItemsRead).
                                         where(UserFeedItemsRead.user_id == user_id,
                                               UserFeedItemsRead.feed_item_id == feed_item_id,
                                               UserFeedItemsRead.feed_id == feed_id)).scalar()
        self.db.delete(user_feed_item)
        self.db.commit()

    def user_feed_item_favorite_exists(self, user_id, feed_id, feed_item_id):
        query = select(UserFeedItemsFavorite).where(UserFeedItemsFavorite.feed_item_id == feed_item_id,
                                                    UserFeedItemsFavorite.user_id == user_id,
                                                    UserFeedItemsFavorite.feed_id == feed_id)
        is_exist = self.db.execute(
            exists(query).select()).scalar_one()
        return is_exist

    def like_action(self, user_id, feed_id, feed_item_id):
        user_feed_item = UserFeedItemsFavorite(user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id)
        self.db.add(user_feed_item)
        self.db.commit()

    def dislike_action(self, user_id, feed_id, feed_item_id):
        user_feed_item = self.db.execute(select(UserFeedItemsFavorite).
                                         where(UserFeedItemsFavorite.user_id == user_id,
                                               UserFeedItemsFavorite.feed_item_id == feed_item_id),
                                         UserFeedItemsFavorite.feed_id == feed_id).scalar()
        self.db.delete(user_feed_item)
        self.db.commit()

    def get_all_feed_items(self, user_id, feed_id):
        is_read_feed_item_ids = self.db.execute(
            select(UserFeedItemsRead.feed_item_id).where(UserFeedItemsRead.user_id == user_id,
                                                         UserFeedItemsRead.feed_id == feed_id)).scalars().all()

        is_liked_feed_item_ids = self.db.execute(
            select(UserFeedItemsFavorite.feed_item_id).where(UserFeedItemsFavorite.user_id == user_id,
                                                             UserFeedItemsFavorite.feed_id == feed_id)).scalars().all()

        is_read_case = case([(FeedItem.id.in_(is_read_feed_item_ids), True)],
                            else_=False).label("is_read")

        is_liked_case = case([(FeedItem.id.in_(is_liked_feed_item_ids), True)],
                             else_=False).label("is_liked")

        feed_items_query = select(FeedItem.id, FeedItem.title, FeedItem.link, FeedItem.updated_feed_item,
                                  FeedItem.summary, FeedItem.created_at, is_read_case, is_liked_case).where(
            FeedItem.feed_id == feed_id)

        return paginate(self.db, feed_items_query)

    def count_unread_feed_items(self, user_id, feed_id):
        is_read_feed_item_ids = self.db.execute(
            select(UserFeedItemsRead.feed_item_id).where(UserFeedItemsRead.user_id == user_id,
                                                         UserFeedItemsRead.feed_id == feed_id)).scalars().all()

        unread_count = self.db.execute(
            select(func.count(FeedItem.id)).where(FeedItem.id.notin_(is_read_feed_item_ids),
                                                  FeedItem.feed_id == feed_id)).scalar()

        return unread_count

    def create_comment(self, user_id, feed_item_id, text):
        user_feed_item_comment = UserFeedItemsComment(user_id=user_id, feed_item_id=feed_item_id, text=text)
        self.db.add(user_feed_item_comment)
        self.db.commit()

    def read_comments(self, user_id, feed_item_id):
        comments = self.db.execute(
            select(UserFeedItemsComment.id, UserFeedItemsComment.text, UserFeedItemsComment.created_at).where(
                UserFeedItemsComment.user_id == user_id,
                UserFeedItemsComment.feed_item_id == feed_item_id)).all()
        return comments

    def comment_exist(self, user_id, feed_item_id, comment_id):
        query = select(UserFeedItemsComment).where(UserFeedItemsComment.user_id == user_id,
                                                   UserFeedItemsComment.feed_item_id == feed_item_id,
                                                   UserFeedItemsComment.id == comment_id)
        is_exist = self.db.execute(exists(query).select()).scalar_one()

        return is_exist

    def delete_comment(self, user_id, feed_item_id, comment_id):
        user_feed_item_comment = self.db.execute(select(UserFeedItemsComment).
                                                 where(UserFeedItemsComment.user_id == user_id,
                                                       UserFeedItemsComment.feed_item_id == feed_item_id),
                                                 UserFeedItemsComment.id == comment_id).scalar()
        self.db.delete(user_feed_item_comment)
        self.db.commit()
