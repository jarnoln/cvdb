import datetime
# from django.core.urlresolvers import reverse
from django.contrib import auth
from django.test import TestCase
from viewcv.models import Cv, Personal, Work


class CvModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv(user=user, name='cv', title='CV')
        cv.save()
        self.assertEqual(Cv.objects.all().count(), 1)
        self.assertEqual(Cv.objects.all()[0], cv)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(str(cv), cv.name)

    def test_url(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.get_absolute_url(), '/cv/%d/' % cv.id)

    def test_get_personal_info(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.personal, None)
        personal = Personal.objects.create(cv=cv, email='richard.hendriks@mail.com', phone='(912) 555 - 4321',
                                           url='http://richardhendricks.example.com',
                                           summary='Richard hails from Tulsa',
                                           image='http://richardhendricks.example.com/richard.png')
        self.assertEqual(cv.personal, personal)

    def test_list_works(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.work_set.count(), 0)
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter')
        self.assertEqual(cv.work_set.count(), 1)
        self.assertEqual(cv.work_set.first(), work)

    def test_can_edit_only_if_creator(self):
        creator = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=creator, name='cv', title='CV')
        self.assertTrue(cv.can_edit(creator))
        user = auth.get_user_model().objects.create(username='random')
        self.assertFalse(cv.can_edit(user))


class PersonalModelTest(TestCase):
    def test_can_save_and_load(self):
        creator = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=creator, name='cv', title='CV')
        info = Personal(cv=cv, phone='(912) 555 - 4321', url='http://richardhendricks.example.com',
                        summary='Richard hails from Tulsa', image='http://richardhendricks.example.com/richard.png')
        info.save()
        self.assertEqual(Personal.objects.all().count(), 1)
        self.assertEqual(Personal.objects.all()[0], info)


class WorkModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        work = Work(cv=cv, name='Daily Bugle', position='Reporter')
        work.save()
        self.assertEqual(Work.objects.all().count(), 1)
        self.assertEqual(Work.objects.all()[0], work)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter')
        self.assertEqual(str(work), '{}:{}'.format(work.name, work.position))

    def test_duration(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2000, 2, 1))
        self.assertEqual(work.duration_years, 0)
        self.assertEqual(work.duration_months, 1)
        self.assertEqual(work.duration_str, '1 month')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2001, 1, 1))
        self.assertEqual(work.duration_years, 1)
        self.assertEqual(work.duration_months, 0)
        self.assertEqual(work.duration_str, '1 year')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2001, 2, 1))
        self.assertEqual(work.duration_years, 1)
        self.assertEqual(work.duration_months, 1)
        self.assertEqual(work.duration_str, '1 year, 1 month')

        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2002, 3, 1))
        self.assertEqual(work.duration_years, 2)
        self.assertEqual(work.duration_months, 2)
        self.assertEqual(work.duration_str, '2 years, 2 months')

        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 6, 1),
                                   end_date=datetime.date(2002, 3, 1))
        self.assertEqual(work.duration_years, 1)
        self.assertEqual(work.duration_months, 9)
        self.assertEqual(work.duration_str, '1 year, 9 months')
