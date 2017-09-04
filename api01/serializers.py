from rest_framework import serializers
from viewcv.models import Cv, Personal, Work, Education, Project, Volunteer


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
        fields = ['cv', 'name', 'position', 'url', 'summary', 'start_date', 'end_date']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['cv', 'institution', 'url', 'area', 'study_type', 'gpa', 'summary', 'start_date', 'end_date']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['cv', 'name', 'description', 'url', 'entity', 'type', 'start_date', 'end_date']


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['cv', 'organization', 'position', 'url', 'summary', 'start_date', 'end_date']
