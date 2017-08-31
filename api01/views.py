from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from viewcv.models import Cv, Work
from .serializers import WorkSerializer


@api_view(['POST'])
def submit_resume(request):
    """ Submit trace """
    data = JSONParser().parse(request)
    work_list = data['work']
    for work_item in work_list:
        serial_data = work_item
        serial_data['start_date'] = work_item['startDate']
        serial_data['end_date'] = work_item['endDate']
        work_serializer = WorkSerializer(data=serial_data)
        if work_serializer.is_valid():
            work_serializer.save()
        else:
            return JsonResponse(work_serializer.errors, status=400)

    return JsonResponse(data, status=201, safe=False)
