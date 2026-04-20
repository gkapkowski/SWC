from django.urls import path, re_path
from .views import shorten, resolve

urlpatterns = [
    path("shorten/", shorten),
    # TODO: make sure the regex matches the possible values of short ids
    re_path("s/(?P<short_id>[0-9a-zA-Z=]+)$", resolve, name="shrt"),
]
