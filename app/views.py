from django.shortcuts import render
from .models import NSE_DATA
from .helperView import getData, RefrestData

# Create your views here.


def HomePage(request):
    if not NSE_DATA.objects.all():
        getData()
    else:
        RefrestData()
    return render(request, "index.html")
