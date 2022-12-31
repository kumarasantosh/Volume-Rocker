from django.urls import path, include
from rest_framework import routers
from .views import VolumeRockerViewSet


router = routers.DefaultRouter()
router.register(r"", VolumeRockerViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
