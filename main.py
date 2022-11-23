import logging.config
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from src.entities.user.handlers import router as user_router
from src.entities.feed.handlers import router as feed_router
from src.config import get_settings
from src.database import init_db

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(title="FeedReader",
              description="""This is FeedReader Application""",
              version="0.0.1",
              docs_url=get_settings().DocUrl)

app.include_router(user_router)
app.include_router(feed_router)


add_pagination(app)


@app.on_event("startup")
def startup_event():
    init_db()
