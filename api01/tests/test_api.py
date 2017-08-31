import json
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


class SubmitResumeTest(TestCase):
    def test_submit_resume(self):
        resume = {
            "basics": {
                "label": "Journalist",
                "summary": ""
            },
            "work": [
                {
                    "company": "Daily Bugle",
                    "position": "Reporter",
                    "startDate": "1945-01-01",
                    "endDate": "2020-01-01",
                    "summary": "Specialized in Superman stories",
                }
            ]
        }

        resume_json = json.dumps(resume)
        self.assertEqual(Work.objects.count(), 0)
        response = self.client.post('/api/01/resume/', data=resume_json, content_type='application/json')
        self.assertEqual(Work.objects.count(), 1)
        work_1 = Work.objects.first()
        # print(response.content)
        data = json.loads(response.content.decode('utf8'))
        # print(data)
        self.assertEqual(work_1.company, "Daily Bugle")
        self.assertEqual(work_1.position, "Reporter")
        self.assertEqual(work_1.summary, "Specialized in Superman stories")
