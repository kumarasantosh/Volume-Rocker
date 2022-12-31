from django.urls import path, include
from rest_framework import routers
from .views import NSE_DATA_VIEW_SET, AddCoi


router = routers.DefaultRouter()
router.register(r"", NSE_DATA_VIEW_SET)
urlpatterns = [
    path("data/", include(router.urls)),
    path("", AddCoi)
]
