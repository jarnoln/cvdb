import json
import datetime
from django.test import TestCase
from django.core.files.base import File
from viewcv.models import Cv, Work
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


def get_resume():
    resume = {
        "basics": {
            "label": "Journalist",
            "summary": "Applying for JLA"
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


class SubmitResumeFileTest(ExtTestCase):
    def test_submit_resume_file(self):
        user = self.create_and_log_in_user()
        resume_file = open('example_resume.json', 'r')
        resume_file_object = File(resume_file, name='example_resume.json')
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        data = {'json_file': resume_file_object}
        response = self.client.post('/api/01/submit_resume_file/', data)
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
