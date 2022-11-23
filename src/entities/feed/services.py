from datetime import datetime
from .repositories import FeedItemRepository, FeedRepository, UserFeedRepository, UserFeedItemsRepository
from .schemas import UnreadCountFeedItemsDTO
from ...utils import FeedsApiInvoke
from .errors import FeedExistsError, FeedSelectedBeforeError, FeedNotSelectedBeforeError, FeedItemIsReadBeforeError, \
    FeedItemIsUnReadBeforeError, FeedItemIsLikedBeforeError, FeedItemIsDislikedBeforeError, CommentNotFoundError
from .models import FeedItem


class FeedService:
    def __init__(self, db_session):
        self.feed_repo = FeedRepository(db_session)

    def feed_creation(self, feed_data):
        feed_exist = self.feed_repo.get_feed_exist(feed_data.rss_link)
        if not feed_exist:
            self.feed_repo.create_feed(feed_data)
        else:
            raise FeedExistsError()

    def show_all_feeds(self):
        return self.feed_repo.get_all_feeds()


class FeedItemsService:
    def __init__(self, db_session):
        self.feed_item_repo = FeedItemRepository(db_session)
        self.feed_repo = FeedRepository(db_session)

    def add_items_to_feeds(self):
        feeds = self.feed_repo.get_all_updatable_feeds()
        feed_parser = FeedsApiInvoke()
        if feeds:
            for feed in feeds:
                parsed_feed = feed_parser.get_feed(feed.rss_link)
                if not parsed_feed:
                    self.feed_repo.update_feed(feed.id, {"updatable": False})
                    continue
                feed_items = parsed_feed.entries
                for item in feed_items:
                    feed_item_last_published = datetime(*item.get('updated_parsed', 'published_parsed')[:6])
                    if not feed.last_updated or feed_item_last_published > feed.last_updated:
                        self.feed_item_repo.add_feed_item(feed.id, item, feed_item_last_published)

                self.feed_item_repo.feed_item_bulk_insert()
                feed_last_updated = datetime.utcnow()
                update_fields = {"last_updated": feed_last_updated, "link": parsed_feed.feed.link}
                self.feed_repo.update_feed(feed.id, update_fields)


class UserFeedService:
    def __init__(self, db_session, user_id, feed_id=None):
        self.user_feed_repo = UserFeedRepository(db_session)
        self.user_id = user_id
        self.feed_id = feed_id

    def select_feed(self):
        if self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id):
            raise FeedSelectedBeforeError()
        else:
            self.user_feed_repo.select_feed_by_user(user_id=self.user_id, feed_id=self.feed_id)

    def deselect_feed(self):
        if not self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id):
            raise FeedNotSelectedBeforeError()
        else:
            self.user_feed_repo.deselect_feed_by_user(user_id=self.user_id, feed_id=self.feed_id)

    def select_feed_by_user(self, select_dto):
        if select_dto.is_selected:
            self.select_feed()
        else:
            self.deselect_feed()

    def user_all_feeds(self):
        return self.user_feed_repo.read_all_user_feeds(user_id=self.user_id)


class UserFeedItemsService:
    def __init__(self, db_session, user_id, feed_id=None, feed_item_id=None):
        self.user_feed_repo = UserFeedRepository(db_session)
        self.user_feed_items_repo = UserFeedItemsRepository(db_session)
        self.user_id = user_id
        self.feed_id = feed_id
        self.feed_item_id = feed_item_id

    def feed_item_read(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            user_feed_item_exist = self.user_feed_items_repo.user_feed_item_read_exists(self.user_id, self.feed_id,
                                                                                        self.feed_item_id)
            if user_feed_item_exist:
                raise FeedItemIsReadBeforeError()
            else:
                self.user_feed_items_repo.read_action(user_id=self.user_id, feed_id=self.feed_id,
                                                      feed_item_id=self.feed_item_id)
        else:
            raise FeedNotSelectedBeforeError()

    def feed_item_unread(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            user_feed_item_read_exist = self.user_feed_items_repo.user_feed_item_read_exists(self.user_id, self.feed_id,
                                                                                             self.feed_item_id)
            if not user_feed_item_read_exist:
                raise FeedItemIsUnReadBeforeError()
            else:
                self.user_feed_items_repo.unread_action(user_id=self.user_id, feed_id=self.feed_id,
                                                        feed_item_id=self.feed_item_id)
        else:
            raise FeedNotSelectedBeforeError()

    def feed_item_like(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            user_feed_item_favorite_exist = self.user_feed_items_repo.user_feed_item_favorite_exists(self.user_id,
                                                                                                     self.feed_id,
                                                                                                     self.feed_item_id)
            if user_feed_item_favorite_exist:
                raise FeedItemIsLikedBeforeError()
            else:
                self.user_feed_items_repo.like_action(user_id=self.user_id, feed_id=self.feed_id,
                                                      feed_item_id=self.feed_item_id)
        else:
            raise FeedNotSelectedBeforeError()

    def feed_item_dislike(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            user_feed_item_favorite_exist = self.user_feed_items_repo.user_feed_item_favorite_exists(self.user_id,
                                                                                                     self.feed_id,
                                                                                                     self.feed_item_id)
            if not user_feed_item_favorite_exist:
                raise FeedItemIsDislikedBeforeError()
            else:
                self.user_feed_items_repo.dislike_action(user_id=self.user_id, feed_id=self.feed_id,
                                                         feed_item_id=self.feed_item_id)
        else:
            raise FeedNotSelectedBeforeError()

    def user_feed_items(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            user_feed_items = self.user_feed_items_repo.get_all_feed_items(user_id=self.user_id, feed_id=self.feed_id)
            return user_feed_items

        else:
            raise FeedNotSelectedBeforeError()

    def user_unread_feed_items_count(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            user_feed_items_unread_count = self.user_feed_items_repo.count_unread_feed_items(user_id=self.user_id,
                                                                                             feed_id=self.feed_id)
            return {"unread_count": user_feed_items_unread_count}
        else:
            raise FeedNotSelectedBeforeError()

    def create_feed_item_comment(self, text):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            self.user_feed_items_repo.create_comment(user_id=self.user_id, feed_item_id=self.feed_item_id, text=text)
        else:
            raise FeedNotSelectedBeforeError()

    def read_feed_item_comments(self):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            return self.user_feed_items_repo.read_comments(user_id=self.user_id, feed_item_id=self.feed_item_id)
        else:
            raise FeedNotSelectedBeforeError()

    def delete_feed_item_comment(self, comment_id):
        user_feed_exist = self.user_feed_repo.user_feed_exists(user_id=self.user_id, feed_id=self.feed_id)
        if user_feed_exist:
            comment_exist = self.user_feed_items_repo.comment_exist(user_id=self.user_id,
                                                                    feed_item_id=self.feed_item_id,
                                                                    comment_id=comment_id)
            if comment_exist:
                self.user_feed_items_repo.delete_comment(user_id=self.user_id, feed_item_id=self.feed_item_id,
                                                         comment_id=comment_id)
            else:
                raise CommentNotFoundError()
        else:
            raise FeedNotSelectedBeforeError()
