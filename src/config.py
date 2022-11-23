import os
from enum import Enum
from functools import lru_cache

from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from pydantic import BaseSettings

load_dotenv()
bearer_scheme = HTTPBearer()


class Settings(BaseSettings):
    DocUrl: str = "/swagger"
    DatabaseURL: str = os.getenv("DATABASE_URL")
    AccessTokenExpireDays = 1
    RefreshTokenExpireDays = 10
    JWTAlgorithm = "HS256"
    JWTSecretKey = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    BrokerURL = os.getenv("BROKER_URL")
    FeedTaskPeriodSeconds = 30


class TokenType(Enum):
    AccessToken = "AccessToken"
    RefreshToken = "RefreshToken"


@lru_cache()
def get_settings():
    return Settings()
