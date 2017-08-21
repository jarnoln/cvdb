from django.test import TestCase
from django.core.urlresolvers import reverse


class SignupTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('account_signup'), '/accounts/signup/')

    def test_default_content(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse('account_signup'))
        self.assertTemplateUsed(response, 'account/signup.html')


class LoginTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('account_login'), '/accounts/login/')

    def test_default_content(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(response, 'account/login.html')
