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
        # Work.objects.create(company=work_item['company'], position=work_item['position'], summary=work_item['summary'])
        work_serializer = WorkSerializer(data=work_item)
        if work_serializer.is_valid():
            work_serializer.save()
        else:
            return JsonResponse(work_serializer.errors, status=400)

    return JsonResponse(data, status=201, safe=False)
    # serializer = TraceSerializer(data=data)
    # if serializer.is_valid():
    #    serializer.save()
    #    return JsonResponse(serializer.data, status=201)
    # else:
    #    return JsonResponse(serializer.errors, status=400)
