from rest_framework import serializers
from app.models import NSE_DATA


class NSE_DATA_SERIALIZERS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NSE_DATA
        fields = ("__all__")
