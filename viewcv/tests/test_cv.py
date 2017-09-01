from django.core.urlresolvers import reverse
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Cv


class CvListTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('cv_list'), '/cvs/')

    def test_uses_correct_template(self):
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


class CvDetailTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('cv', args=['1']), '/cv/1/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv', args=[cv.id]))
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')

    def test_default_content(self):
        user = self.create_and_log_in_user()
        cv = Cv.objects.create(name='test_cv', title='Test CV', user=user)
        response = self.client.get(reverse('cv', args=[cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cv'], cv)
        self.assertContains(response, cv.title)
