from django.test import TestCase
from django.core.urlresolvers import reverse


class UploadCvTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('upload'), '/upload/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('upload'))
        self.assertTemplateUsed(response, 'viewcv/upload.html')
