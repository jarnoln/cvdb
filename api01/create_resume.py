from django.http import JsonResponse
from viewcv.models import Cv, Work
from .serializers import CvSerializer, PersonalSerializer, WorkSerializer, EducationSerializer, VolunteerSerializer
from .serializers import ProjectSerializer


def create_resume(data, user):
    cv = Cv.objects.create(user=user, summary=data['basics']['summary'], title=data['basics']['label'])
    personal_data = data['basics']
    personal_data['cv'] = cv.id
    personal_serializer = PersonalSerializer(data=personal_data)
    if personal_serializer.is_valid():
        personal_serializer.save()
    else:
        return JsonResponse(personal_serializer.errors, status=400)

    work_list = data.get('work', [])
    for work_item in work_list:
        work_data = work_item
        work_data['cv'] = cv.id
        work_data['start_date'] = work_item['startDate']
        work_data['end_date'] = work_item['endDate']
        work_serializer = WorkSerializer(data=work_data)
        if work_serializer.is_valid():
            work_serializer.save()
        else:
            return JsonResponse(work_serializer.errors, status=400)

    education_list = data.get('education', [])
    for education_item in education_list:
        education_data = education_item
        education_data['cv'] = cv.id
        education_data['study_type'] = education_item['studyType']
        education_data['start_date'] = education_item['startDate']
        education_data['end_date'] = education_item['endDate']
        education_serializer = EducationSerializer(data=education_data)
        if education_serializer.is_valid():
            education_serializer.save()
        else:
            return JsonResponse(education_serializer.errors, status=400)

    volunteer_list = data.get('volunteer', [])
    for item in volunteer_list:
        volunteer_data = item
        volunteer_data['cv'] = cv.id
        volunteer_data['start_date'] = item['startDate']
        volunteer_data['end_date'] = item['endDate']
        volunteer_serializer = VolunteerSerializer(data=volunteer_data)
        if volunteer_serializer.is_valid():
            volunteer_serializer.save()
        else:
            return JsonResponse(volunteer_serializer.errors, status=400)

    project_list = data.get('projects', [])
    for item in project_list:
        project_data = item
        project_data['cv'] = cv.id
        project_data['start_date'] = item['startDate']
        project_data['end_date'] = item['endDate']
        project_serializer = ProjectSerializer(data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
        else:
            return JsonResponse(project_serializer.errors, status=400)

    if cv:
        cv_serializer = CvSerializer(cv)
        return JsonResponse(cv_serializer.data, status=201, safe=False)
    else:
        return JsonResponse(data, status=201, safe=False)
