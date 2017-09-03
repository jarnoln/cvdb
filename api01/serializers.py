from rest_framework import serializers
from viewcv.models import Cv, Work


class CvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cv
        fields = ['id', 'name', 'title', 'summary']


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['cv', 'company', 'position', 'website', 'start_date', 'end_date', 'summary']
