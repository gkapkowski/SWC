import pytest
from django.test.client import RequestFactory
from shortener.models import ShortURL
from shortener.serializers import ShortenOutputSerializer


@pytest.mark.django_db
def test_output_serializer():
    req = RequestFactory().get("/")

    obj = ShortURL.objects.create(original="http://example.com/")
    s = ShortenOutputSerializer(obj, context={"request": req})
    assert s.get_short_url(obj) == "http://testserver/s/AQ"
