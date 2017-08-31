from rest_framework import serializers
from viewcv.models import Cv, Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['cv', 'company', 'position', 'start_date', 'end_date', 'summary']
