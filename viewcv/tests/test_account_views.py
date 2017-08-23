from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import auth


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

    def test_signup(self):
        self.assertEqual(auth.models.User.objects.count(), 0)
        response = self.client.post(reverse('account_signup'), {
            'username': 'user',
            'email': 'user@iki.fi',
            'password1': 'password',
            'password2': 'password'}, follow=True)
        self.assertEqual(auth.models.User.objects.count(), 1)
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertEqual(response.context['user'], auth.models.User.objects.first())
        html = response.content.decode('utf8')
        self.assertInHTML('Logout', html)


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

    def test_login(self):
        user = auth.models.User.objects.create(username='user', email='user@iki.fi')
        user.set_password('password')
        user.save()
        response = self.client.post(reverse('account_login'), {
            'login': user.username,
            'password': 'password',
            'next': reverse('home')}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertEqual(response.context['user'], user)
        html = response.content.decode('utf8')
        self.assertInHTML('Logout', html)


class ProfileTest(TestCase):
    def create_and_log_in_user(self):
        user = auth.models.User.objects.create(username='test_user', email='tuser@iki.fi')
        user.set_password('password')
        user.save()
        response = self.client.post(reverse('account_login'), {'login': user.username, 'password': 'password'})
        html = response.content.decode('utf8')
        print(html)
        return user

    def test_reverse(self):
        self.assertEqual(reverse('profile'), '/accounts/profile/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'viewcv/profile.html')
