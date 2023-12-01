import logging

from poc_gcp_django.cloud_celery import app

logger = logging.getLogger(__name__)


@app.task
def hello(name: str):
    logger.info(f"task hello executed with name {name}")



