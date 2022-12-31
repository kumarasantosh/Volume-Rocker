from django.shortcuts import render
from rest_framework import viewsets
from .models import VolumeRocker
from .serializers import VolumeRockerSerializer
import datetime
# Create your views here.


class VolumeRockerViewSet(viewsets.ModelViewSet):
    queryset = VolumeRocker.objects.all().filter(
        Date=datetime.datetime.today()).order_by("-Diffrence15Min")
    serializer_class = VolumeRockerSerializer
