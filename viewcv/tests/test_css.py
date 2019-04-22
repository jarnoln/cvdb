import datetime
# from unittest import skip
from django.contrib import auth
from django.urls import reverse
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Cv, Personal, Css, CssUrl, Work, Education, Volunteer, Skill, Language, Project


class CssListTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('css_list'), '/css_list/')

    def test_uses_correct_template(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('css_list'))
        self.assertTemplateUsed(response, 'viewcv/css_list.html')

    def test_default_content(self):
        user = self.create_and_log_in_user()
        response = self.client.get(reverse('css_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['css_list'].count(), 0)
        cv = Css.objects.create(name='test_css', title='Test CSS', creator=user)
        response = self.client.get(reverse('css_list'))
        self.assertEqual(response.context['css_list'].count(), 1)
        self.assertEqual(response.context['css_list'][0], cv)
        self.assertContains(response, cv.title)
        Css.objects.create(name='test_css_2', title='Test CSS 2', creator=user)
        response = self.client.get(reverse('css_list'))
        self.assertEqual(response.context['css_list'].count(), 2)
