from django.urls import reverse
from django.core.files.base import File
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Css


class UploadCvTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('upload_css'), '/upload-css/')

    def test_uses_correct_template(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('upload_css'))
        self.assertTemplateUsed(response, 'viewcv/upload_css.html')

    def test_submit_small_css_file(self):
        user = self.create_and_log_in_user()
        css_file = open('examples/basic.css', 'r')
        css_file_object = File(css_file, name='basic.css')
        self.assertEqual(Css.objects.count(), 0)
        data = {'css_file': css_file_object}
        response = self.client.post(reverse('upload_css'), data, follow=True)
        # print(response.content)
        self.assertEqual(Css.objects.count(), 1)
        css = Css.objects.first()
        self.assertEqual(css.name, "default")
        # print(css.css)
        self.assertTrue(str(css.css).startswith('@media print '))
