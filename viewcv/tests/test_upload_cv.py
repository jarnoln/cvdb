from django.urls import reverse
from django.core.files.base import File
from users.tests.ext_test_case import ExtTestCase
from viewcv.models import Cv, Personal, Work, Education, Volunteer, Skill, Language, Project


class UploadCvTest(ExtTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('upload'), '/upload/')

    def test_uses_correct_template(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse('upload'))
        self.assertTemplateUsed(response, 'viewcv/upload.html')

    def test_submit_small_resume_file(self):
        user = self.create_and_log_in_user()
        resume_file = open('examples/small.json', 'r')
        resume_file_object = File(resume_file, name='small.json')
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        data = {'json_file': resume_file_object}
        response = self.client.post(reverse('upload'), data, follow=True)
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        cv = Cv.objects.first()
        self.assertEqual(cv.user, user)
        self.assertEqual(cv.name, "default")
        self.assertEqual(cv.summary, 'A summary of Clark Kent')
        self.assertEqual(Work.objects.count(), 1)
        work_1 = Work.objects.all()[0]
        self.assertEqual(work_1.cv, cv)
        self.assertEqual(work_1.name, "Daily Bugle")
        self.assertEqual(work_1.position, "Reporter")
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')
        self.assertEqual(response.context['cv'], cv)

    def test_submit_complete_resume_file(self):
        user = self.create_and_log_in_user()
        resume_file = open('examples/complete.json', 'r')
        resume_file_object = File(resume_file, name='complete.json')
        self.assertEqual(Cv.objects.count(), 0)
        self.assertEqual(Work.objects.count(), 0)
        data = {'json_file': resume_file_object}
        response = self.client.post(reverse('upload'), data, follow=True)
        # print(response.content)
        self.assertEqual(Cv.objects.count(), 1)
        cv = Cv.objects.first()
        self.assertEqual(cv.user, user)
        self.assertEqual(cv.name, "default")
        self.assertTrue(cv.summary.startswith, 'Richard hails from Tulsa.')
        self.assertEqual(Personal.objects.count(), 1)
        personal = Personal.objects.first()
        self.assertEqual(personal.cv, cv)
        self.assertEqual(personal.image, '')
        self.assertEqual(personal.email, 'richard.hendriks@mail.com')
        self.assertEqual(personal.phone, '(912) 555-4321')
        self.assertEqual(personal.url, 'http://richardhendricks.example.com')
        self.assertTrue(personal.summary.startswith, 'Richard hails from Tulsa.')
        self.assertEqual(Work.objects.count(), 1)
        work = Work.objects.all()[0]
        self.assertEqual(work.cv, cv)
        self.assertEqual(work.name, "Pied Piper")
        self.assertEqual(work.position, "CEO/President")
        self.assertEqual(Education.objects.count(), 1)
        edu = Education.objects.all()[0]
        self.assertEqual(edu.cv, cv)
        self.assertEqual(edu.institution, "University of Oklahoma")
        self.assertEqual(edu.area, "Information Technology")
        self.assertEqual(edu.study_type, "Bachelor")
        self.assertEqual(edu.gpa, "4.0")
        self.assertTemplateUsed(response, 'viewcv/cv_detail.html')
        self.assertEqual(response.context['cv'], cv)
        self.assertEqual(Volunteer.objects.count(), 1)
        volunteer = Volunteer.objects.all()[0]
        self.assertEqual(volunteer.cv, cv)
        self.assertEqual(volunteer.organization, "CoderDojo")
        self.assertEqual(volunteer.position, "Teacher")
        self.assertEqual(Skill.objects.count(), 2)
        skill = Skill.objects.all()[0]
        self.assertEqual(skill.cv, cv)
        self.assertEqual(skill.name, "Compression")
        self.assertEqual(skill.level, "Master")
        self.assertEqual(Language.objects.count(), 1)
        language = Language.objects.all()[0]
        self.assertEqual(language.cv, cv)
        self.assertEqual(language.name, "English")
        self.assertEqual(language.fluency, "Native speaker")
        project = Project.objects.all()[0]
        self.assertEqual(project.cv, cv)
        self.assertEqual(project.name, "Miss Direction")
        self.assertEqual(project.description, "A mapping engine that misguides you")
