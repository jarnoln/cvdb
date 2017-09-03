from django.core.urlresolvers import reverse
from django.core.files.base import File
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Cv, Work


class UploadCvTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('upload'), '/upload/')

    def test_uses_correct_template(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('upload'))
        self.assertTemplateUsed(response, 'viewcv/upload.html')

    def test_submit_resume_file(self):
        user = self.create_and_log_in_user()
        resume_file = open('example_resume.json', 'r')
        resume_file_object = File(resume_file, name='example_resume.json')
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        data = {'json_file': resume_file_object}
        response = self.client.post(reverse('upload'), data, follow=True)
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        cv = Cv.objects.first()
        self.assertEqual(cv.user, user)
        self.assertEqual(cv.name, "default")
        self.assertEqual(cv.summary, 'A summary of Clark Kent')
        self.assertEqual(Work.objects.count(), 1)
        work_1 = Work.objects.all()[0]
        self.assertEqual(work_1.cv, cv)
        self.assertEqual(work_1.company, "Daily Bugle")
        self.assertEqual(work_1.position, "Reporter")
        self.assertTemplateUsed(response, 'viewcv/upload.html')
