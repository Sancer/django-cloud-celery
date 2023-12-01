import logging
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.views import View

from tasks.tasks import hello

logger = logging.getLogger(__name__)


class PingView(View):
    def get(self, request):
        hello.delay(name="test")
        hello.apply_async(name="test_delay", eta=datetime.now() + timedelta(minutes=5))

        return HttpResponse("ping")

