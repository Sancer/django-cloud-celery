import json

from django.http import HttpResponse
from django.views import View

import logging

from django_cloud_celery import CloudCelery

logger = logging.getLogger(__name__)


class CloudTaskConsumerView(View):
    cloud_celery: CloudCelery = None

    async def post(self, request, *args, **kwargs):
        queue = kwargs.get("task_name")
        payload = json.loads(request.body)
        logger.info("Received task in consumer view", extra={"task_name": queue, "payload": payload})
        self.cloud_celery.consume(queue, payload)
        return HttpResponse()
