from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from stats.models import Country
from stats.serializers import CountrySerializer


class CountryViewSet(viewsets.ViewSet):
    """
    Public ViewSet for listing or retrieving country and live statistics.
    """
    def list(self, request: Request) -> Response:
        """
        Return a list of all countries with daily live statistics.
        """
        queryset = Country.objects.prefetch_related('live_statistics')
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        """
        Return a object of country with daily live statistics.
        """
        queryset = Country.objects.all()
        country = get_object_or_404(queryset, pk=pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)
