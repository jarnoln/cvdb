import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from viewcv.models import Cv, Work
from .serializers import CvSerializer, WorkSerializer


def create_resume(data, user):
    work_list = data['work']
    if len(work_list) > 0:
        cv = Cv.objects.create(user=user, summary=data['basics']['summary'], title=data['basics']['label'])
        for work_item in work_list:
            serial_data = work_item
            serial_data['cv'] = cv.id
            serial_data['start_date'] = work_item['startDate']
            serial_data['end_date'] = work_item['endDate']
            work_serializer = WorkSerializer(data=serial_data)
            if work_serializer.is_valid():
                work_serializer.save()
            else:
                return JsonResponse(work_serializer.errors, status=400)

    if cv:
        cv_serializer = CvSerializer(cv)
        return JsonResponse(cv_serializer.data, status=201, safe=False)
    else:
        return JsonResponse(data, status=201, safe=False)


@api_view(['POST'])
def submit_resume(request):
    """ Submit resume """
    data = JSONParser().parse(request)
    response = create_resume(data, request.user)
    return response


@api_view(['POST'])
def submit_resume_file(request):
    """ Submit resume """
    resume_file = request.FILES['json_file']
    # print('resume file=%s' % resume_file)
    file_content = resume_file.read()
    data = json.loads(file_content.decode('utf-8'))
    response = create_resume(data, request.user)
    return response
