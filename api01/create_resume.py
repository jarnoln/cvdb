import json
from django.http import JsonResponse
from viewcv.models import Cv, Work
from .serializers import CvSerializer, PersonalSerializer, WorkSerializer, EducationSerializer, VolunteerSerializer
from .serializers import SkillSerializer, LanguageSerializer, ProjectSerializer


def create_resume(data, user):
    cv = Cv.objects.create(user=user, summary=data['basics']['summary'], title=data['basics']['label'])
    personal_data = data['basics']
    personal_data['cv'] = cv.id
    if 'profiles' in data['basics']:
        personal_data['profiles'] = json.dumps(data['basics']['profiles'], sort_keys=True)
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
        if work_data['end_date'] == '':
            work_data['end_date'] = '1337-01-01'
        work_serializer = WorkSerializer(data=work_data)
        if work_serializer.is_valid():
            work_serializer.save()
        else:
            return JsonResponse(work_serializer.errors, status=400)

        work_object = Work.objects.get(cv=cv, name=work_item['name'])
        work_projects = work_data.get('projects', [])
        for work_project in work_projects:
            project_data = work_project
            project_data['cv'] = cv.id
            project_data['work'] = work_object.id
            project_data['start_date'] = work_project['startDate']
            project_data['end_date'] = work_project['endDate']
            if project_data['end_date'] == '':
                project_data['end_date'] = '1337-01-01'
            if 'keywords' in work_project:
                project_data['keywords'] = json.dumps(work_project['keywords'])
            else:
                project_data['keywords'] = json.dumps([])

            project_data['keywords'] = work_project.get('keywords', '[]')
            if project_data['end_date'] == '':
                project_data['end_date'] = '1337-01-01'

            project_serializer = ProjectSerializer(data=project_data)
            if project_serializer.is_valid():
                project_serializer.save()
            else:
                return JsonResponse(project_serializer.errors, status=400)

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

    skill_list = data.get('skills', [])
    for item in skill_list:
        skill_data = item
        skill_data['cv'] = cv.id
        if 'keywords' in item:
            skill_data['keywords'] = json.dumps(item['keywords'])

        skill_serializer = SkillSerializer(data=skill_data)
        if skill_serializer.is_valid():
            skill_serializer.save()
        else:
            return JsonResponse(skill_serializer.errors, status=400)

    language_list = data.get('languages', [])
    for item in language_list:
        language_data = item
        language_data['cv'] = cv.id
        if 'language' in item:
            language_data['name'] = item['language']

        language_serializer = LanguageSerializer(data=language_data)
        if language_serializer.is_valid():
            language_serializer.save()
        else:
            return JsonResponse(language_serializer.errors, status=400)

    project_list = data.get('projects', [])
    for item in project_list:
        project_data = item
        project_data['cv'] = cv.id
        project_data['work'] = None
        if 'keywords' in item:
            project_data['keywords'] = json.dumps(item['keywords'])
        else:
            project_data['keywords'] = json.dumps([])
        # project_data['keywords'] = item.get('keywords', '[]')
        project_data['start_date'] = item['startDate']
        project_data['end_date'] = item['endDate']
        if project_data['end_date'] == '':
            project_data['end_date'] = '1337-01-01'
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
