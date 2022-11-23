from sqlalchemy import select

from .models import User


class UserRepository:

    def __init__(self, db_session):
        self.db = db_session

    def get_user_by_email(self, user_email):
        return self.db.execute(select(User).where(User.email == user_email)).scalar()

    def get_user_by_id(self, user_id):
        return self.db.execute(select(User.id, User.email, User.is_active, User.created_at).where(User.id == user_id
                                                                                                  )).first()

    def create_user(self, user_email, hashed_password):
        new_user = User(
            email=user_email,
            hashed_password=hashed_password
        )

        self.db.add(new_user)
        self.db.commit()
        return new_user.id
