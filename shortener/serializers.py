from rest_framework import serializers
from .models import ShortURL


class ShortenInputSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=1000)


class ShortenOutputSerializer(serializers.Serializer):
    short_url = serializers.SerializerMethodField()
    url = serializers.URLField(source="original")

    def get_short_url(self, obj: ShortURL):
        return self.context["request"].build_absolute_uri(obj.short_path)
