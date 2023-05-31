from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "longitude",
                OpenApiTypes.FLOAT,
                description="Longitude, to search the nearest point",
                required=False,
            ),
            OpenApiParameter(
                "latitude",
                OpenApiTypes.FLOAT,
                description="Latitude, to search the nearest point",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        longitude = request.query_params.get("longitude")
        latitude = request.query_params.get("latitude")

        if longitude and latitude:
            point = Point(float(longitude), float(latitude), srid=4326)
            return self.nearest(point)

        return super().list(request, *args, **kwargs)

    def nearest(self, point: Point):
        nearest_place = (
            self.queryset.annotate(distance=Distance("geom", point))
            .order_by("distance")
            .first()
        )

        if not nearest_place:
            return Response(
                {"message": "No nearest place found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.get_serializer(nearest_place).data, status=status.HTTP_200_OK
        )
