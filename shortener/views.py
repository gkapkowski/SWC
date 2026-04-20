import logging
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import ShortURL
from .serializers import ShortenInputSerializer, ShortenOutputSerializer


log = logging.getLogger("shorten.views")


@api_view(http_method_names=["POST"])
def shorten(request: Request) -> Response:
    data = ShortenInputSerializer(data=request.data)
    data.is_valid(raise_exception=True)

    short_url = ShortURL.objects.create(original=data.validated_data["url"])

    return Response(
        ShortenOutputSerializer(instance=short_url, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(http_method_names=["GET"])
def resolve(request: Request, short_id: str) -> Response:
    try:
        short_url = ShortURL.objects.get(id=ShortURL.short_id_to_id(short_id=short_id))
    except ShortURL.DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_302_FOUND, headers={"location": short_url.original})
