from celery import Celery
from src.config import get_settings
from src.entities.feed.tasks import add_feed_items

app = Celery(broker=f"{get_settings().BrokerURL}",
             include=['src.entities.feed.tasks']
             )


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(get_settings().FeedTaskPeriodSeconds, add_feed_items.s(),
                             name=f'add every {get_settings().FeedTaskPeriodSeconds} seconds')
