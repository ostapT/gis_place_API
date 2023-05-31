from django.urls import include, path
from rest_framework import routers
from .views import PlaceViewSet

router = routers.DefaultRouter()
router.register("places", PlaceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "place_app"
