import json
import datetime
from django.test import TestCase
from django.core.files.base import File
from viewcv.models import Cv, Personal, Work, Education, Volunteer, Skill, Language, Project
from users.tests.ext_test_case import ExtTestCase


class ApiRootTest(TestCase):
    def test_default_content(self):
        response = self.client.get('/api/01/')
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Api Root')
        response_string = response.content.decode('utf8')
        data = json.loads(response_string)
        # print(data)
        # self.assertEqual(data['process'], 'http://testserver/api/01/process/')
        # self.assertEqual(data['drive'], 'http://testserver/api/01/drive/')


def get_work_bugle():
    work = {
        "name": "Daily Bugle",
        "position": "Reporter",
        "startDate": "1945-01-01",
        "endDate": "2020-01-01",
        "summary": "Specialized in Superman stories",
    }
    return work


def get_education():
    education = {
        "institution": "Smallville College",
        "area": "Journalism",
        "studyType": "Bachelor",
        "startDate": "1940-06-01",
        "endDate": "1944-01-01",
        "gpa": "3.5",
        "url": "http://college.smallville.org",
        "summary": "Summary",
        "courses": [
            "J101 - Introduction to Journalism",
            "J201 - Advanced Journalism"
        ]
    }
    return education


def get_volunteer_work():
    volunteer_work = {
        "organization": "CoderDojo",
        "position": "Teacher",
        "url": "http://coderdojo.example.com/",
        "startDate": "2012-01-01",
        "endDate": "2013-01-01",
        "summary": "Global movement of free coding clubs for young people.",
        "highlights": [
            "Awarded 'Teacher of the Month'"
        ]
    }
    return volunteer_work


def get_resume():
    resume = {
        "basics": {
            "name": "Clark Kent",
            "label": "Journalist",
            "image": "http://clark.kent.com/clark.jpg",
            "email": "clark.kent@dailybugle.com",
            "phone": "(912) 555-4321",
            "url": "http://clark.kent.com",
            "summary": "Clark Kent grew up in Kansas.",
            "profiles": [
                {
                    "network": "Twitter",
                    "username": "clarkkent",
                    "url": ""
                },
                {
                    "network": "SoundCloud",
                    "username": "clarkkent",
                    "url": "https://soundcloud.example.com/clarkkent"
                }
            ]
        },
        "work": []
    }
    return resume


class SubmitResumeTest(ExtTestCase):
    def test_submit_resume_with_two_work_entries(self):
        user = self.create_and_log_in_user()
        resume = get_resume()
        work_1_data = get_work_bugle()
        work_2_data = {
            "name": "Jonah's farm",
            "position": "Farmhand",
            "url": "http://www.jonahs-farm.com",
            "startDate": "1940-01-01",
            "endDate": "1944-12-01",
            "summary": "Helping my parents at farm",
        }
        resume['work'] = [work_1_data, work_2_data]
        resume_json = json.dumps(resume)
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        cv = Cv.objects.first()
        self.assertEqual(cv.user, user)
        self.assertEqual(cv.name, "default")
        self.assertEqual(cv.title, "Journalist")
        self.assertEqual(cv.summary, resume['basics']['summary'])
        self.assertEqual(Personal.objects.count(), 1)
        self.assertEqual(cv.summary, resume['basics']['summary'])
        personal = Personal.objects.first()
        self.assertEqual(personal.cv, cv)
        self.assertEqual(personal.image, resume['basics']['image'])
        self.assertEqual(personal.email, resume['basics']['email'])
        self.assertEqual(personal.phone, resume['basics']['phone'])
        self.assertEqual(personal.url, resume['basics']['url'])
        self.assertEqual(personal.profiles, json.dumps(resume['basics']['profiles'], sort_keys=True))
        self.assertEqual(personal.summary, resume['basics']['summary'])
        self.assertEqual(Work.objects.count(), 2)
        work_1 = Work.objects.all()[0]
        work_2 = Work.objects.all()[1]
        data = json.loads(response.content.decode('utf8'))
        # print(data)
        self.assertEqual(data['id'], cv.id)
        self.assertEqual(work_1.cv, cv)
        self.assertEqual(work_1.name, "Daily Bugle")
        self.assertEqual(work_1.position, "Reporter")
        self.assertEqual(work_1.summary, "Specialized in Superman stories")
        self.assertEqual(work_1.start_date, datetime.date(1945, 1, 1))
        self.assertEqual(work_1.end_date, datetime.date(2020, 1, 1))

        self.assertEqual(work_2.cv, cv)
        self.assertEqual(work_2.name, "Jonah's farm")
        self.assertEqual(work_2.position, "Farmhand")
        self.assertEqual(work_2.url, "http://www.jonahs-farm.com")
        self.assertEqual(work_2.summary, "Helping my parents at farm")
        self.assertEqual(work_2.start_date, datetime.date(1940, 1, 1))
        self.assertEqual(work_2.end_date, datetime.date(1944, 12, 1))

    def test_submit_work_with_no_end_date_set(self):
        user = self.create_and_log_in_user()
        resume = get_resume()
        work_data = get_work_bugle()
        work_data['endDate'] = ''
        resume['work'] = [work_data]
        resume_json = json.dumps(resume)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        self.assertEqual(Work.objects.count(), 1)
        work_1 = Work.objects.all()[0]
        self.assertEqual(work_1.start_date, datetime.date(1945, 1, 1))
        self.assertEqual(work_1.end_date, datetime.date(1337, 1, 1))  # Special date, replaced by current date in UI
        today = datetime.date.today()
        self.assertEqual(work_1.duration_years, today.year - work_1.start_date.year)
        self.assertEqual(work_1.duration_months, today.month - work_1.start_date.month)

    def test_submit_resume_with_education(self):
        user = self.create_and_log_in_user()
        resume = get_resume()
        education = get_education()
        resume['education'] = [education]
        resume_json = json.dumps(resume)
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Education.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        self.assertEqual(Education.objects.count(), 1)
        edu = Education.objects.first()
        self.assertEqual(edu.institution, education['institution'])
        self.assertEqual(edu.url, education['url'])
        self.assertEqual(edu.area, education['area'])
        self.assertEqual(edu.gpa, education['gpa'])
        self.assertEqual(edu.study_type, education['studyType'])
        self.assertEqual(edu.summary, education['summary'])
        self.assertEqual(edu.start_date, datetime.date(1940, 6, 1))
        self.assertEqual(edu.end_date, datetime.date(1944, 1, 1))

    def test_submit_resume_with_ongoing_education(self):
        user = self.create_and_log_in_user()
        resume = get_resume()
        education = get_education()
        education['endDate'] = ''
        resume['education'] = [education]
        resume_json = json.dumps(resume)
        self.assertEqual(Education.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        self.assertEqual(Education.objects.count(), 1)
        edu = Education.objects.first()
        self.assertEqual(edu.start_date, datetime.date(1940, 6, 1))
        self.assertEqual(edu.end_date, datetime.date(1337, 1, 1))

    def test_submit_resume_with_volunteer_work(self):
        self.create_and_log_in_user()
        resume = get_resume()
        volunteer_data = get_volunteer_work()
        resume['volunteer'] = [volunteer_data]
        resume_json = json.dumps(resume)
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Volunteer.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        self.assertEqual(Volunteer.objects.count(), 1)
        cv = Cv.objects.first()
        volunteer = Volunteer.objects.first()
        self.assertEqual(volunteer.cv, cv)
        self.assertEqual(volunteer.organization, volunteer_data['organization'])
        self.assertEqual(volunteer.position, volunteer_data['position'])
        self.assertEqual(volunteer.url, volunteer_data['url'])
        self.assertEqual(volunteer.summary, volunteer_data['summary'])
        self.assertEqual(volunteer.start_date, datetime.date(2012, 1, 1))
        self.assertEqual(volunteer.end_date, datetime.date(2013, 1, 1))

    def test_submit_resume_with_ongoing_volunteer_work(self):
        self.create_and_log_in_user()
        resume = get_resume()
        volunteer_data = get_volunteer_work()
        volunteer_data['endDate'] = ''
        resume['volunteer'] = [volunteer_data]
        resume_json = json.dumps(resume)
        self.assertEqual(Volunteer.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        self.assertEqual(Volunteer.objects.count(), 1)
        cv = Cv.objects.first()
        volunteer = Volunteer.objects.first()
        self.assertEqual(volunteer.cv, cv)
        self.assertEqual(volunteer.start_date, datetime.date(2012, 1, 1))
        self.assertEqual(volunteer.end_date, datetime.date(1337, 1, 1))

    def test_submit_resume_with_skill(self):
        self.create_and_log_in_user()
        resume = get_resume()
        skill_data = {
            "name": "Compression",
            "level": "Master",
            "keywords": [
                "Mpeg",
                "MP4",
                "GIF"
            ]
        }
        resume['skills'] = [skill_data]
        resume_json = json.dumps(resume)
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Skill.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        self.assertEqual(Cv.objects.count(), 1)
        self.assertEqual(Skill.objects.count(), 1)
        cv = Cv.objects.first()
        skill = Skill.objects.first()
        self.assertEqual(skill.cv, cv)
        self.assertEqual(skill.name, skill_data['name'])
        self.assertEqual(skill.level, skill_data['level'])

    def test_submit_resume_with_language(self):
        self.create_and_log_in_user()
        resume = get_resume()
        data = {
            "language": "English",
            "fluency": "Native",
        }
        resume['languages'] = [data]
        resume_json = json.dumps(resume)
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Language.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        self.assertEqual(Cv.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 1)
        cv = Cv.objects.first()
        language = Language.objects.first()
        self.assertEqual(language.cv, cv)
        self.assertEqual(language.name, data['language'])
        self.assertEqual(language.fluency, data['fluency'])

    def test_submit_resume_with_project(self):
        self.create_and_log_in_user()
        resume = get_resume()
        project_data = {
            "name": "Miss Direction",
            "description": "A mapping engine that misguides you",
            "highlights": [
                "Won award at AIHacks 2016",
                "Built by all women team of newbie programmers",
                "Using modern technologies such as GoogleMaps, Chrome Extension and Javascript"
            ],
            "keywords": [
                "GoogleMaps", "Chrome Extension", "Javascript"
            ],
            "industry": "Consumer",
            "client": "Navigore",
            "startDate": "2016-08-24",
            "endDate": "2016-08-24",
            "url": "http://missdirection.example.com",
            "roles": [
                "Team lead", "Designer"
            ],
            "entity": "Smoogle",
            "type": "application"
        }
        resume['projects'] = [project_data]
        resume_json = json.dumps(resume)
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Project.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, project_data['name'])
        self.assertEqual(project.description, project_data['description'])
        self.assertEqual(project.url, project_data['url'])
        self.assertEqual(project.entity, project_data['entity'])
        self.assertEqual(project.type, project_data['type'])
        self.assertEqual(project.keywords, json.dumps(project_data['keywords']))
        self.assertEqual(project.industry, project_data['industry'])
        self.assertEqual(project.client, project_data['client'])
        self.assertEqual(project.start_date, datetime.date(2016, 8, 24))
        self.assertEqual(project.end_date, datetime.date(2016, 8, 24))


class SubmitSmallResumeFileTest(ExtTestCase):
    def test_submit_resume_file(self):
        user = self.create_and_log_in_user()
        resume_file = open('examples/small.json', 'r')
        resume_file_object = File(resume_file, name='small.json')
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        data = {'json_file': resume_file_object}
        self.client.post('/api/01/submit_resume_file/', data)
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        cv = Cv.objects.first()
        self.assertEqual(cv.user, user)
        self.assertEqual(cv.name, "default")
        self.assertEqual(cv.summary, 'A summary of Clark Kent')
        self.assertEqual(Work.objects.count(), 1)
        work_1 = Work.objects.all()[0]
        self.assertEqual(work_1.cv, cv)
        self.assertEqual(work_1.name, "Daily Bugle")
        self.assertEqual(work_1.position, "Reporter")


class SubmitCompleteResumeFileTest(ExtTestCase):
    def test_submit_resume_file(self):
        user = self.create_and_log_in_user()
        resume_file = open('examples/complete.json', 'r')
        resume_file_object = File(resume_file, name='complete.json')
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        data = {'json_file': resume_file_object}
        self.client.post('/api/01/submit_resume_file/', data)
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        cv = Cv.objects.first()
        self.assertEqual(cv.user, user)
        self.assertEqual(cv.name, "default")
        self.assertTrue(cv.summary.startswith, 'Richard hails from Tulsa.')
        self.assertEqual(Work.objects.count(), 1)
        work_1 = Work.objects.all()[0]
        self.assertEqual(work_1.cv, cv)
        self.assertEqual(work_1.name, "Pied Piper")
        self.assertEqual(work_1.position, "CEO/President")
