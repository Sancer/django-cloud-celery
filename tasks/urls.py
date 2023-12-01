from django.urls import path

from tasks.views import PingView


urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
]
