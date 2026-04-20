import base64
import math
import logging
from django.utils.functional import cached_property
from django.urls import reverse
from django.db import models

log = logging.getLogger("shortener.models")


class ShortURL(models.Model):
    # id: using autoincrement field prevents reusing row ids but is prone to enumeration attacks, would be better to use some randowm numbers/uuid
    # but this would increase size of short id significantly
    id = models.BigAutoField(primary_key=True)
    original = models.URLField(max_length=1000)

    @cached_property
    def short_id(self) -> str:
        """Note: it's possible to switch to Base62 encoding to get rid of - and _ chars"""

        # Get integer bytes aligned to smallest possible size
        id_bytes = self.id.to_bytes(math.ceil(self.id.bit_length() / 8))
        # Get base64 string with trimmed padding
        return base64.urlsafe_b64encode(id_bytes).decode("ascii").replace("=", "")

    @cached_property
    def short_path(self) -> str:
        """Returns proper path currently configured in urls to handle the redirection logic"""
        return reverse("shrt", kwargs=dict(short_id=self.short_id))

    @classmethod
    def short_id_to_id(cls, short_id: str):
        """Returns database row ID converted from base64 encoded string"""
        return int.from_bytes(base64.urlsafe_b64decode(short_id + "=" * (-len(short_id) % 4)))
