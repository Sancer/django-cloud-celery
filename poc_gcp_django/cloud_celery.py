from django.conf import settings

from django_cloud_celery import CloudCelery


app = CloudCelery(settings.PROJECT_ID, settings.LOCATION, settings.SERVICE_DOMAIN, queue=settings.SERVICE_NAME)

