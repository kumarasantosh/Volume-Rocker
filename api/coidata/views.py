from django.shortcuts import render
from rest_framework import viewsets
from .models import NseDataCoi
from .serializers import NSE_DATA_SERIALIZERS
from .helperView import RefrestData, getData, refrestVolumeRockerData
import schedule
from api.VolumeRocker.models import VolumeRocker
import time
from background_task import background

# Create your views here.


class NSE_DATA_VIEW_SET(viewsets.ModelViewSet):
    queryset = NseDataCoi.objects.all().order_by("strikePrice")
    serializer_class = NSE_DATA_SERIALIZERS


@background(schedule=60)
def NseData():
    print("heyyyy")
    if not NseDataCoi.objects.all():
        getData()
    else:
        RefrestData()


@background(schedule=60)
def VolumeRockers():
    print("workingggg")
    if not VolumeRocker.objects.all():
        refrestVolumeRockerData()
    else:
        refrestVolumeRockerData()


def AddCoi(request):
    NseData(repeat=60, verbose_name="NseData")
    VolumeRockers(repeat=120, verbose_name="VolumeRockers")

    return render(request, "add.html")
