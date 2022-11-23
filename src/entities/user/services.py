from datetime import datetime, timedelta
from passlib.context import CryptContext
from .errors import UserRegisteredBeforeError, PasswordNotMatchError, UserDoesNotExist
from src.config import get_settings, TokenType
from .repositories import UserRepository
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenGenerator:

    @staticmethod
    def get_token_expire(token_type: TokenType):
        if token_type == TokenType.AccessToken:
            return get_settings().AccessTokenExpireDays
        elif token_type == TokenType.RefreshToken:
            return get_settings().RefreshTokenExpireDays

    def create_token(self, data: dict, token_type: TokenType):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.get_token_expire(token_type))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, get_settings().JWTSecretKey, algorithm=get_settings().JWTAlgorithm)
        return encoded_jwt

    def get_tokens(self, payload):
        access_token = self.create_token(payload, TokenType.AccessToken)
        refresh_token = self.create_token(payload, TokenType.RefreshToken)
        data = {"access_token": access_token, "refresh_token": refresh_token}
        return data


class UserService:
    def __init__(self, db_session):
        self.user_repo = UserRepository(db_session)

    def register_user(self, user_data):
        user = self.user_repo.get_user_by_email(user_data.email)
        if user:
            raise UserRegisteredBeforeError()
        else:
            user_id = self.user_repo.create_user(user_data.email, self.get_password_hash(user_data.password))
            token_data = {"user_id": user_id, "email": user_data.email}
            token_generator = TokenGenerator()
            return token_generator.get_tokens(token_data)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    def login_user(self, user_data):
        user = self.user_repo.get_user_by_email(user_data.email)
        if user:
            hashed_password = self.verify_password(user_data.password, user.hashed_password)
            if hashed_password:
                token_data = {"user_id": user.id, "email": user.email}
                token_generator = TokenGenerator()
                return token_generator.get_tokens(token_data)
            else:
                raise PasswordNotMatchError()
        else:
            raise UserDoesNotExist()

    def get_user_info(self, user_id):
        user = self.user_repo.get_user_by_id(user_id)
        if user:
            return user
        else:
            raise UserDoesNotExist()
