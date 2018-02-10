from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('home'), '/')

    def test_default_content(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CVDB')
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'viewcv/upload.html')
