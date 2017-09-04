from django.http import JsonResponse
from viewcv.models import Cv, Work
from .serializers import CvSerializer, PersonalSerializer, WorkSerializer


def create_resume(data, user):
    work_list = data['work']
    if len(work_list) > 0:
        cv = Cv.objects.create(user=user, summary=data['basics']['summary'], title=data['basics']['label'])
        personal_data = data['basics']
        personal_data['cv'] = cv.id
        personal_serializer = PersonalSerializer(data=personal_data)
        if personal_serializer.is_valid():
            personal_serializer.save()
        else:
            return JsonResponse(personal_serializer.errors, status=400)

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
