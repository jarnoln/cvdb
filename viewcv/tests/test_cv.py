import datetime
# from unittest import skip
from django.contrib import auth
from django.core.urlresolvers import reverse
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Cv, Personal, Work, Education, Volunteer, Skill, Language, Project


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
        self.assertEqual(reverse('cv_public', args=['user']), '/u/user/cv/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')

    def test_public_cv(self):
        creator = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=creator, public=True, primary=True)
        response = self.client.get(reverse('cv_public', args=[creator.username]))
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')

    def test_default_content(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        personal = Personal.objects.create(cv=cv, email='richard.hendriks@mail.com', phone='(912) 555 - 4321',
                                           url='http://richardhendricks.example.com',
                                           summary='Richard hails from Tulsa',
                                           image='http://richardhendricks.example.com/richard.png')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter', url='http://dailybugle.com',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2001, 2, 1))
        education = Education.objects.create(cv=cv, institution='University of Oklahoma', area="IT",
                                             study_type='Bachelor', gpa='4.0',
                                             start_date=datetime.date(2011, 6, 1),
                                             end_date=datetime.date(2014, 1, 1))
        volunteer = Volunteer.objects.create(cv=cv, organization='CoderDojo', position="Teacher",
                                             url='http://coderdojo.example.com/',
                                             summary='Global movement of free coding clubs for young people.',
                                             start_date=datetime.date(2012, 1, 1),
                                             end_date=datetime.date(2013, 1, 1))
        skill = Skill.objects.create(cv=cv, name='Compression', level='Master', keywords='["MPEG","MP4","GIF"]')
        language = Language.objects.create(cv=cv, name='English', fluency='Native')
        project = Project.objects.create(cv=cv, name='Miss Direction',
                                         description="A mapping engine that misguides you",
                                         type='application',
                                         start_date=datetime.date(2016, 8, 24),
                                         end_date=datetime.date(2016, 8, 24))

        response = self.client.get(reverse('cv', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cv'], cv)
        self.assertContains(response, cv.title)
        self.assertContains(response, personal.email)
        self.assertContains(response, personal.phone)
        self.assertContains(response, personal.url)
        self.assertContains(response, personal.summary)
        self.assertContains(response, work.name)
        self.assertContains(response, work.position)
        self.assertContains(response, work.url)
        self.assertContains(response, education.institution)
        self.assertContains(response, education.study_type)
        self.assertContains(response, volunteer.organization)
        self.assertContains(response, volunteer.position)
        self.assertContains(response, volunteer.url)
        self.assertContains(response, volunteer.summary)
        self.assertContains(response, skill.name)
        self.assertContains(response, language.name)
        self.assertContains(response, project.name)
        self.assertContains(response, project.url)
        self.assertContains(response, project.description)


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

