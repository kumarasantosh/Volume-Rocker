from rest_framework import serializers
from .models import NseDataCoi


class NSE_DATA_SERIALIZERS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NseDataCoi
        fields = ("__all__")
