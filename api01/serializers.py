from rest_framework import serializers
from viewcv.models import Cv, Personal, Work, Education


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


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['cv', 'institution', 'area', 'study_type', 'gpa', 'start_date', 'end_date']
