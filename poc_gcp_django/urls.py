
from django.contrib import admin
from django.urls import path, include

from django_cloud_celery.views import CloudTaskConsumerView
from poc_gcp_django.cloud_celery import app

urlpatterns = [
    path("cloud-tasks-consumer/<task_name>/", CloudTaskConsumerView.as_view(cloud_celery=app), name="cloud-tasks-consumer"),
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
]
