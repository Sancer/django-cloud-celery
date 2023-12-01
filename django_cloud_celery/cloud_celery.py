from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable

from django.urls import resolve, reverse
from google.api_core.exceptions import FailedPrecondition, AlreadyExists
from google.cloud import tasks_v2

from django_cloud_celery.task import Task

logger = logging.getLogger(__name__)


class CloudCelery:

    def __init__(self, project_id, location, service_domain, queue, debug=False):
        self.project_id = project_id
        self.location = location
        self.service_domain = service_domain
        self.queue = queue
        self.debug = debug

        self.tasks_client = tasks_v2.CloudTasksClient()

        self._tasks = {}

    def task(self, func) -> Callable:
        def wrapper(eta: datetime = None, *args, **kwargs):
            logger.info("Executing task")
            if self.debug:
                logger.info("Executing task in debug mode (sync)")
                func(*args, **kwargs)
                return

            logger.info("Executing task in production mode (async)")
            self._push_task(self._build_task(func, eta=eta, *args, **kwargs))

        def delay(*args, **kwargs):
            apply_async(*args, **kwargs)

        def apply_async(eta: datetime = None, *args, **kwargs):
            wrapper(eta, *args, **kwargs)

        logger.info("Registering task")
        func = func
        self._tasks[func.__name__] = func

        wrapper.delay = delay
        wrapper.apply_async = apply_async

        return wrapper

    def consume(self, queue: str, payload) -> None:
        self._tasks[queue](**payload)

    def _build_task(self, func, *args, **kwargs) -> Task:
        task_name = func.__name__
        url_path = reverse("cloud-tasks-consumer", args=[task_name])
        tasks_consumer_url = f"{self.service_domain}{url_path}"
        return Task(
            task_name=task_name,
            url=tasks_consumer_url,
            eta=kwargs.pop("eta", None),
            payload=kwargs if kwargs else None,
        )

    def _push_task(self, task: Task) -> None:
        logger.info("Pushing task", extra={"task_id": task.id})
        cloud_task = tasks_v2.Task(
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.POST,
                url=task.url,
                headers={"Content-type": "application/json"},
                body=task.payload_to_json().encode(),
            ),
            name=(
                self.tasks_client.task_path(self.project_id, self.location, self.queue, task.id)
            ),
        )

        if task.eta is not None:
            cloud_task.schedule_time = task.eta_to_timestamp_pb2()

        try:
            self._dispatch_task(cloud_task=cloud_task)
        except FailedPrecondition as e:
            logger.info("Queue not found, creating it", extra={"queue": task.task_name})
            self._create_queue(task.task_name)
            self._dispatch_task(cloud_task=cloud_task)
        logger.info("Task pushed", extra={"task_id": task.id})

    def _dispatch_task(self, cloud_task: tasks_v2.Task) -> None:
        self.tasks_client.create_task(
            tasks_v2.CreateTaskRequest(
                parent=self.tasks_client.queue_path(self.project_id, self.location, self.queue),
                task=cloud_task,
            )
        )

    def _create_queue(self, queue_name: str) -> None:
        create_queue_request = tasks_v2.CreateQueueRequest(
            parent=self.tasks_client.common_location_path(self.project_id, self.location),
            queue=tasks_v2.Queue(name=self.tasks_client.queue_path(self.project_id, self.location, queue_name)),
        )
        try:
            self.tasks_client.create_queue(create_queue_request)
        except AlreadyExists as e:
            logger.info("Queue already exists", extra={"queue": queue_name})
            pass


