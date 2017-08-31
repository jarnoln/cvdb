from rest_framework import serializers
from viewcv.models import Cv, Work


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Work
        fields = ['company', 'position', 'summary']
