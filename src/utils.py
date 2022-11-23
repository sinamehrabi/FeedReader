import feedparser
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
import requests
import backoff
from fastapi import HTTPException, Depends, status
from jose import jwt

from src.config import bearer_scheme, get_settings


class ApiInvoke(ABC):

    @abstractmethod
    def _get_data(self, url, headers):
        pass


class Adapter(ABC):

    @abstractmethod
    def get_req(self, url, headers):
        pass


class RequestAdapter(Adapter):

    def get_req(self, url, headers):
        resp = requests.get(url=url, headers=headers)
        if 200 <= resp.status_code < 300:
            return resp.content


class FeedsApiInvoke(ApiInvoke):
    def __init__(self):
        self.adapter = RequestAdapter()

    def _get_data(self, url, headers=None):
        return self.adapter.get_req(url, headers)

    @staticmethod
    def request_give_up_handler(error, *args, **kwargs) -> Any:
        logging.error(error)

    @backoff.on_exception(backoff.expo, Exception, max_tries=2,
                          giveup=request_give_up_handler,
                          raise_on_giveup=False)
    def get_feed(self, url):
        try:
            data = self._get_data(url)
            return feedparser.parse(data)
        except (requests.exceptions.RequestException, AttributeError) as err:
            logging.error(err)


def verify_token(token: str = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(token.credentials, get_settings().JWTSecretKey, algorithms=[get_settings().JWTAlgorithm])
        return payload['user_id']
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized, {e}"
        )


def get_current_datetime():
    return datetime.utcnow()
