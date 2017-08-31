import json
import datetime
from django.test import TestCase
from viewcv.models import Cv, Work


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
        "company": "Daily Bugle",
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
            "summary": ""
        },
        "work": []
    }
    return resume


class SubmitResumeTest(TestCase):
    def test_submit_resume_with_two_work_entries(self):
        resume = get_resume()
        work_1 = get_work_bugle()
        work_2 = {
            "company": "Jonah's farm",
            "position": "Farmhand",
            "startDate": "1940-01-01",
            "endDate": "1944-12-01",
            "summary": "Helping my parents at farm",
        }
        resume['work'] = [work_1, work_2]
        resume_json = json.dumps(resume)
        self.assertEqual(Work.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        self.assertEqual(Work.objects.count(), 2)
        work_1 = Work.objects.all()[0]
        work_2 = Work.objects.all()[1]
        # print(response.content)
        data = json.loads(response.content.decode('utf8'))
        # print(data)
        self.assertEqual(work_1.company, "Jonah's farm")
        self.assertEqual(work_1.position, "Farmhand")
        self.assertEqual(work_1.summary, "Helping my parents at farm")
        self.assertEqual(work_1.start_date, datetime.date(1940, 1, 1))
        self.assertEqual(work_1.end_date, datetime.date(1944, 12, 1))
        self.assertEqual(work_2.company, "Daily Bugle")
        self.assertEqual(work_2.position, "Reporter")
        self.assertEqual(work_2.summary, "Specialized in Superman stories")
        self.assertEqual(work_2.start_date, datetime.date(1945, 1, 1))
        self.assertEqual(work_2.end_date, datetime.date(2020, 1, 1))
