from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Place

PLACE_LIST_URL = "place_app:place-list"
PLACE_DETAIL_URL = "place_app:place-detail"


class PlaceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.place1 = Place.objects.create(
            name="Place 1",
            description="Description 1",
            geom=Point(10.3344, 30.3344),
        )
        self.place2 = Place.objects.create(
            name="Place 2",
            description="Description 2",
            geom=Point(20.3344, 30.3344),
        )

    def test_list_places(self):
        url = reverse(PLACE_LIST_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_place(self):
        url = reverse(PLACE_DETAIL_URL, args=[self.place1.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 1)

    def test_create_place(self):
        url = reverse(PLACE_LIST_URL)
        data = {
            "name": "New Place",
            "description": "New Description",
            "longitude": 40.3344,
            "latitude": 50.3344,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)

    def test_update_place(self):
        url = reverse(PLACE_DETAIL_URL, args=[self.place1.pk])
        data = {
            "name": "Updated Place",
            "description": "Updated Description",
            "longitude": 60.3344,
            "latitude": 70.3344,
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["longitude"], data["longitude"])
        self.assertEqual(response.data["latitude"], data["latitude"])

    def test_find_nearest_place(self):
        url = reverse("place_app:place-nearest")
        params = {"longitude": 30.0, "latitude": 40.0}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place1.name)
        self.assertEqual(response.data["description"], self.place1.description)
