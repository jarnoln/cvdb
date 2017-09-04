import datetime
# from unittest import skip
from django.contrib import auth
from django.core.urlresolvers import reverse
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Cv, Work


class CvListTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('cv_list'), '/cvs/')

    def test_uses_correct_template(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('cv_list'))
        self.assertTemplateUsed(response, 'viewcv/cv_list.html')

    def test_default_content(self):
        user = self.create_and_log_in_user()
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cv_list'].count(), 0)
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.context['cv_list'].count(), 1)
        self.assertEqual(response.context['cv_list'][0], cv)
        self.assertContains(response, cv.title)
        Cv.objects.create(name='test_cv_2', title='Test CV 2', user=user)
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.context['cv_list'].count(), 2)

    def test_list_only_own_cvs(self):
        user = self.create_and_log_in_user()
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.context['cv_list'].count(), 0)
        another_user = auth.get_user_model().objects.create(username='another_user')
        cv_1 = Cv.objects.create(name='test_cv', title='Test CV', user=another_user)
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.context['cv_list'].count(), 0)
        cv_2 = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.context['cv_list'].count(), 1)
        self.assertEqual(response.context['cv_list'][0], cv_2)


class CvDetailTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('cv', args=['1337']), '/cv/1337/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')

    def test_default_content(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter', url='http://dailybugle.com',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2001, 2, 1))
        response = self.client.get(reverse('cv', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cv'], cv)
        self.assertContains(response, cv.title)
        self.assertContains(response, work.name)
        self.assertContains(response, work.position)
        self.assertContains(response, work.url)


class UpdateCvTest(ExtTestCase):
    def test_reverse_task_edit(self):
        self.assertEqual(reverse('cv_update', args=['1337']),
                         '/cv/1337/edit/')

    def test_uses_correct_template(self):
        creator = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=creator)
        response = self.client.get(reverse('cv_update', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_form.html')

    def test_default_context(self):
        creator = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=creator)
        response = self.client.get(reverse('cv_update', args=[cv.id]))
        self.assertEqual(response.context['cv'], cv)
        self.assertEqual(response.context['message'], '')

    def test_can_update_cv(self):
        creator = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=creator)
        self.assertEqual(Cv.objects.all().count(), 1)
        response = self.client.post(reverse('cv_update', args=[cv.id]),
                                    {'name': 'updated_name', 'title': 'CV updated'},
                                    follow=True)
        self.assertEqual(Cv.objects.all().count(), 1)
        cv = Cv.objects.all()[0]
        self.assertEqual(cv.name, 'updated_name')
        self.assertEqual(cv.title, 'CV updated')
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')


class DeleteCvTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('cv_delete', args=['1']), '/cv/1/delete/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv_delete', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_confirm_delete.html')

    def test_can_delete_cv(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        self.assertEqual(Cv.objects.all().count(), 1)
        response = self.client.post(reverse('cv_delete', args=[cv.id]), {}, follow=True)
        self.assertEqual(Cv.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'viewcv/cv_list.html')

    def test_404_no_cv(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('cv_delete', args=['1']))
        self.assertTemplateUsed(response, '404.html')

    def test_cant_cv_project_if_not_logged_in(self):
        user = auth.get_user_model().objects.create(username='shinji')
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        self.assertEqual(Cv.objects.all().count(), 1)
        response = self.client.post(reverse('cv_delete', args=[cv.id]), {}, follow=True)
        self.assertEqual(Cv.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_cant_delete_cv_if_not_creator(self):
        creator = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=creator)
        self.assertEqual(Cv.objects.all().count(), 1)
        logged_user = self.create_and_log_in_user()
        response = self.client.post(reverse('cv_delete', args=[cv.id]), {}, follow=True)
        self.assertEqual(Cv.objects.all().count(), 1)
        self.assertTemplateUsed(response, '404.html')

