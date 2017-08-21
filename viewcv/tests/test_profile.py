from django.test import TestCase
from django.core.urlresolvers import reverse


class HomePageTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('profile'), '/accounts/profile/')

    def test_default_content(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'viewcv/profile.html')
