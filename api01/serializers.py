from rest_framework import serializers
from viewcv.models import Cv, Personal, Work


class CvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cv
        fields = ['id', 'name', 'title', 'summary']


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ['cv', 'email', 'phone', 'url', 'image', 'summary']


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['cv', 'name', 'position', 'url', 'start_date', 'end_date', 'summary']
