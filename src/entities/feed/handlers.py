from typing import List

from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from .schemas import CreateFeedDTO, FeedInfoDTO, SelectFeedDTO, FeedItemDTO, UnreadCountFeedItemsDTO, CreateCommentDTO, \
    ReadCommentsDTO
from .services import FeedItemsService, FeedService, UserFeedService, UserFeedItemsService
from ...database import get_db
from ...utils import verify_token

router = APIRouter()


@router.post("/feeds", status_code=status.HTTP_201_CREATED)
def create_feeds(feed_data: CreateFeedDTO, db: Session = Depends(get_db)):
    FeedService(db).feed_creation(feed_data)


@router.get("/feeds", status_code=status.HTTP_200_OK, response_model=Page[FeedInfoDTO])
def get_feeds(db: Session = Depends(get_db)):
    all_feed = FeedService(db).show_all_feeds()
    return all_feed


@router.post("/users/me/feeds/{feed_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_feed_selection(feed_id: int, select_dto: SelectFeedDTO, db: Session = Depends(get_db),
                        user_id: int = Depends(verify_token)):
    UserFeedService(db, user_id=user_id, feed_id=feed_id).select_feed_by_user(select_dto=select_dto)


@router.get("/users/me/feeds", status_code=status.HTTP_200_OK, response_model=Page[FeedInfoDTO],
            response_model_exclude_none=True)
def get_user_feeds(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    return UserFeedService(db, user_id=user_id).user_all_feeds()


@router.post("/users/me/feeds/{feed_id}/items/{feed_item_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def user_feed_is_read(feed_id: int, feed_item_id: int, db: Session = Depends(get_db),
                      user_id: int = Depends(verify_token)):
    UserFeedItemsService(db, user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id).feed_item_read()


@router.delete("/users/me/feeds/{feed_id}/items/{feed_item_id}/unread", status_code=status.HTTP_204_NO_CONTENT)
def user_feed_is_unread(feed_id: int, feed_item_id: int, db: Session = Depends(get_db),
                        user_id: int = Depends(verify_token)):
    UserFeedItemsService(db, user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id).feed_item_unread()


@router.post("/users/me/feeds/{feed_id}/items/{feed_item_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def user_feed_is_favorite(feed_id: int, feed_item_id: int, db: Session = Depends(get_db),
                          user_id: int = Depends(verify_token)):
    UserFeedItemsService(db, user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id).feed_item_like()


@router.delete("/users/me/feeds/{feed_id}/items/{feed_item_id}/dislike", status_code=status.HTTP_204_NO_CONTENT)
def user_feed_is_not_favorite(feed_id: int, feed_item_id: int, db: Session = Depends(get_db),
                              user_id: int = Depends(verify_token)):
    UserFeedItemsService(db, user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id).feed_item_dislike()


@router.get("/users/me/feeds/{feed_id}/items", status_code=status.HTTP_200_OK, response_model=Page[FeedItemDTO])
def user_feed_items(feed_id: int, db: Session = Depends(get_db),
                    user_id: int = Depends(verify_token)):
    return UserFeedItemsService(db, user_id=user_id, feed_id=feed_id).user_feed_items()


@router.get("/users/me/feeds/{feed_id}/unread-count", status_code=status.HTTP_200_OK,
            response_model=UnreadCountFeedItemsDTO)
def user_feed_items_unread_count(feed_id: int, db: Session = Depends(get_db),
                                 user_id: int = Depends(verify_token)):
    return UserFeedItemsService(db, user_id=user_id, feed_id=feed_id).user_unread_feed_items_count()


@router.post("/users/me/feeds/{feed_id}/items/{feed_item_id}/comments", status_code=status.HTTP_204_NO_CONTENT)
def create_feed_item_comment(feed_id: int, feed_item_id: int, comment: CreateCommentDTO, db: Session = Depends(get_db),
                             user_id: int = Depends(verify_token)):
    UserFeedItemsService(db, user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id).create_feed_item_comment(
        comment.text)


@router.get("/users/me/feeds/{feed_id}/items/{feed_item_id}/comments", status_code=status.HTTP_200_OK,
            response_model=List[ReadCommentsDTO])
def read_feed_item_comment(feed_id: int, feed_item_id: int, db: Session = Depends(get_db),
                           user_id: int = Depends(verify_token)):
    return UserFeedItemsService(db, user_id=user_id, feed_id=feed_id,
                                feed_item_id=feed_item_id).read_feed_item_comments()


@router.delete("/users/me/feeds/{feed_id}/items/{feed_item_id}/comments/{comment_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_feed_item_comment(feed_id: int, feed_item_id: int, comment_id: int, db: Session = Depends(get_db),
                             user_id: int = Depends(verify_token)):
    UserFeedItemsService(db, user_id=user_id, feed_id=feed_id, feed_item_id=feed_item_id).delete_feed_item_comment(
        comment_id)
