from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    longitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, write_only=True
    )
    latitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, write_only=True
    )

    class Meta:
        model = Place
        fields = ["id", "name", "description", "geom", "longitude", "latitude"]
        read_only_fields = ["id", "geom"]

    def create(self, validated_data):
        longitude = validated_data.pop("longitude")
        latitude = validated_data.pop("latitude")
        validated_data["geom"] = Point(float(longitude), float(latitude))
        place = Place.objects.create(**validated_data)
        return place

    def update(self, instance, validated_data):
        if "longitude" in validated_data or "latitude" in validated_data:
            longitude = validated_data.pop("longitude", instance.geom.x)
            latitude = validated_data.pop("latitude", instance.geom.y)
            instance.geom = Point(float(longitude), float(latitude))
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
