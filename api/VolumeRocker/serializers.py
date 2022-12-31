from rest_framework import serializers
from .models import VolumeRocker


class VolumeRockerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VolumeRocker
        fields = ("__all__")
