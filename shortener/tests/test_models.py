import pytest
from shortener.models import ShortURL


@pytest.mark.django_db
def test_short_url_id_conversions():
    short_url = ShortURL.objects.create(original="http://example.com/")

    # base64(1) == "AQ=="
    assert short_url.id == 1
    assert short_url.short_id == "AQ"
    assert short_url.short_path == "/s/AQ"
    assert ShortURL.short_id_to_id(short_url.short_id) == short_url.id
