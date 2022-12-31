from django.shortcuts import render
from rest_framework import viewsets
from app.models import NSE_DATA
from .serializers import NSE_DATA_SERIALIZERS

# Create your views here.


class NSE_DATA_VIEW_SET(viewsets.ModelViewSet):
    queryset = NSE_DATA.objects.all()
    serializer_class = NSE_DATA_SERIALIZERS
