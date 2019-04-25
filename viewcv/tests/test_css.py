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


class UpdateCssTest(ExtTestCase):
    def test_reverse_task_edit(self):
        self.assertEqual(reverse('css_update', args=['1337']),
                         '/css/1337/edit/')

    def test_uses_correct_template(self):
        creator = self.create_and_log_in_user()
        css = Css.objects.create(name='test_css', title='Test CSS', creator=creator)
        response = self.client.get(reverse('css_update', args=[css.id]))
        self.assertTemplateUsed(response, 'viewcv/css_form.html')

    def test_default_context(self):
        creator = self.create_and_log_in_user()
        css = Css.objects.create(name='test_css', title='Test CSS', creator=creator)
        response = self.client.get(reverse('css_update', args=[css.id]))
        self.assertEqual(response.context['css'], css)
        self.assertEqual(response.context['message'], '')

    def test_can_update_css(self):
        creator = self.create_and_log_in_user()
        css = Css.objects.create(name='org_name', title='Org title', creator=creator)
        self.assertEqual(css.name, 'org_name')
        self.assertEqual(css.title, 'Org title')
        self.assertEqual(Css.objects.all().count(), 1)
        response = self.client.post(reverse('css_update', args=[css.id]),
                                    {'name': 'updated_name', 'title': 'CV updated'},
                                    follow=True)
        self.assertEqual(Css.objects.all().count(), 1)
        css = Css.objects.all()[0]
        self.assertEqual(css.name, 'updated_name')
        self.assertEqual(css.title, 'CV updated')
        self.assertTemplateUsed(response, 'viewcv/css_form.html')


class DeleteCssTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('css_delete', args=['1']), '/css/1/delete/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        css = Css.objects.create(name='test_css', title='Test CSS', creator=user)
        response = self.client.get(reverse('css_delete', args=[css.id]))
        self.assertTemplateUsed(response, 'viewcv/css_confirm_delete.html')

    def test_can_delete_cv(self):
        user = self.create_and_log_in_user()
        css = Css.objects.create(name='test_css', title='Test CSS', creator=user)
        self.assertEqual(Css.objects.all().count(), 1)
        response = self.client.post(reverse('css_delete', args=[css.id]), {}, follow=True)
        self.assertEqual(Css.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'viewcv/css_list.html')

    def test_404_no_css(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('css_delete', args=['1']))
        self.assertTemplateUsed(response, '404.html')

    def test_cant_delete_css_if_not_logged_in(self):
        user = auth.get_user_model().objects.create(username='shinji')
        css = Css.objects.create(name='test_css', title='Test CSS', creator=user)
        self.assertEqual(Css.objects.all().count(), 1)
        response = self.client.post(reverse('css_delete', args=[css.id]), {}, follow=True)
        self.assertEqual(Css.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_cant_delete_css_if_not_creator(self):
        creator = auth.get_user_model().objects.create(username='creator')
        css = Css.objects.create(name='test_css', title='Test CSS', creator=creator)
        self.assertEqual(Css.objects.all().count(), 1)
        logged_user = self.create_and_log_in_user()
        response = self.client.post(reverse('css_delete', args=[css.id]), {}, follow=True)
        self.assertEqual(Css.objects.all().count(), 1)
        self.assertTemplateUsed(response, '404.html')
