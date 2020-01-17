from unittest import skip
import datetime
from django.contrib import auth
from django.test import TestCase
from viewcv.models import Cv, Personal, Css, CssUrl, Work, Education, Volunteer, Skill, Language, Project


class CvModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv(user=user, name='cv', title='CV')
        cv.save()
        self.assertEqual(Cv.objects.all().count(), 1)
        self.assertEqual(Cv.objects.all()[0], cv)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV', public=False, primary=False)
        self.assertEqual(str(cv), cv.name)

    def test_url(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.get_absolute_url(), '/cv/%d/' % cv.id)

    def test_set_as_primary(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv_1 = Cv.objects.create(user=user, name='cv1', title='CV 1')
        cv_2 = Cv.objects.create(user=user, name='cv2', title='CV 2')
        self.assertEqual(cv_1.primary, False)
        self.assertEqual(cv_2.primary, False)
        cv_1.set_as_primary()
        cv_1 = Cv.objects.get(name='cv1')
        cv_2 = Cv.objects.get(name='cv2')
        self.assertEqual(cv_1.primary, True)
        self.assertEqual(cv_2.primary, False)
        cv_2.set_as_primary()
        cv_1 = Cv.objects.get(name='cv1')
        cv_2 = Cv.objects.get(name='cv2')
        self.assertEqual(cv_2.primary, True)
        self.assertEqual(cv_1.primary, False)

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

    def test_list_educations(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.education_set.count(), 0)
        education = Education.objects.create(cv=cv, institution='University of Oklahoma', area="IT",
                                             study_type='Bachelor', gpa='4.0',
                                             start_date=datetime.date(2011, 6, 1),
                                             end_date=datetime.date(2014, 1, 1))
        self.assertEqual(cv.education_set.count(), 1)
        self.assertEqual(cv.education_set.first(), education)

    def test_list_volunteer_work(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.project_set.count(), 0)
        volunteer = Volunteer.objects.create(cv=cv, organization='CoderDojo', position="Teacher",
                                             url='http://coderdojo.example.com/',
                                             summary='Global movement of free coding clubs for young people.',
                                             start_date=datetime.date(2012, 1, 1),
                                             end_date=datetime.date(2013, 1, 1))
        self.assertEqual(cv.volunteer_set.count(), 1)
        self.assertEqual(cv.volunteer_set.first(), volunteer)

    def test_list_skills(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.skill_set.count(), 0)
        skill = Skill.objects.create(cv=cv, name='Compression', level='Master', keywords='["MPEG","MP4","GIF"]')
        self.assertEqual(cv.skill_set.count(), 1)
        self.assertEqual(cv.skill_set.first(), skill)

    def test_list_specialties(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.skill_set.count(), 0)
        skill_1 = Skill.objects.create(cv=cv, name='Python', level='Excellent')
        skill_2 = Skill.objects.create(cv=cv, name='JavaScript', level='Good')
        self.assertEqual(cv.skill_set.count(), 2)
        self.assertEqual(cv.specialties.count(), 1)
        self.assertEqual(cv.specialties.first(), skill_1)
        self.assertEqual(cv.non_specialties.count(), 1)
        self.assertEqual(cv.non_specialties.first(), skill_2)

    def test_list_languages(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.language_set.count(), 0)
        language = Language.objects.create(cv=cv, name='English', fluency='Native')
        self.assertEqual(cv.language_set.count(), 1)
        self.assertEqual(cv.language_set.first(), language)

    def test_list_projects(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        self.assertEqual(cv.project_set.count(), 0)
        project = Project.objects.create(cv=cv, name='Miss Direction',
                                         description="A mapping engine that misguides you",
                                         type='application',
                                         start_date=datetime.date(2016, 8, 24),
                                         end_date=datetime.date(2016, 8, 24))
        self.assertEqual(cv.project_set.count(), 1)
        self.assertEqual(cv.project_set.first(), project)

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
                        summary='Richard hails from Tulsa', image='http://richardhendricks.example.com/richard.png',
                        profiles='[]')
        info.save()
        self.assertEqual(Personal.objects.all().count(), 1)
        self.assertEqual(Personal.objects.all()[0], info)
        self.assertEqual(len(info.profile_list), 0)

    def test_profiles(self):
        profile_data = '[{"network": "Twitter", "username": "clark", "url": ""},' \
                       '{"network": "SC", "username": "kent", "url": "https://soundcloud.example.com/kent"}]'
        creator = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=creator, name='cv', title='CV')
        info = Personal.objects.create(cv=cv, phone='(912) 555 - 4321', profiles=profile_data)
        profile_list = info.profile_list
        self.assertEqual(len(profile_list), 2)
        self.assertEqual(profile_list[0]['network'], 'Twitter')
        self.assertEqual(profile_list[0]['username'], 'clark')
        self.assertEqual(profile_list[0]['url'], '')
        self.assertEqual(profile_list[1]['network'], 'SC')
        self.assertEqual(profile_list[1]['username'], 'kent')
        self.assertEqual(profile_list[1]['url'], 'https://soundcloud.example.com/kent')


class CssModelTest(TestCase):
    def test_can_save_and_load(self):
        creator = auth.get_user_model().objects.create(username='creator')
        css = Css(creator=creator, name='mycss', title='My CSS', summary='Summary',
                  css='p { font-family: "Times New Roman", Times, serif; }')
        css.save()
        self.assertEqual(Css.objects.all().count(), 1)
        self.assertEqual(Css.objects.all()[0], css)

    def test_string(self):
        creator = auth.get_user_model().objects.create(username='creator')
        css = Css.objects.create(creator=creator, name='mycss', title='My CSS', summary='Summary',
                                 css='p { font-family: "Times New Roman", Times, serif; }')
        # self.assertEqual(str(css), '{}:{}'.format(css.name, css.title))
        self.assertEqual(str(css), css.title)


class CssUrlModelTest(TestCase):
    def test_can_save_and_load(self):
        creator = auth.get_user_model().objects.create(username='creator')
        css_url = CssUrl(creator=creator, name='my_css_url', title='My CSS URL', summary='Summary',
                         url='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css')
        css_url.save()
        self.assertEqual(CssUrl.objects.all().count(), 1)
        self.assertEqual(CssUrl.objects.all()[0], css_url)

    def test_string(self):
        creator = auth.get_user_model().objects.create(username='creator')
        css_url = CssUrl.objects.create(creator=creator, name='my_css_url', title='My CSS URL', summary='Summary',
                                        url='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.css')
        # self.assertEqual(str(css_url), '{}:{}:{}'.format(css_url.name, css_url.title, css_url.url))
        self.assertEqual(str(css_url), css_url.title)


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

    def test_end_date_current(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(2000, 2, 1))
        self.assertEqual(work.end_date_current, work.end_date)
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(1337, 1, 1))
        self.assertEqual(work.end_date_current.year, datetime.date.today().year)

    def test_duration_with_no_end_date(self):
        """ Using date 1337-01-01 should cause it to be replaced by current date in duration calculations """
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(1337, 1, 1))
        self.assertTrue(work.duration_years > 17)
        today = datetime.date.today()
        self.assertEqual(work.duration_months, today.month - work.start_date.month)

    def test_work_projects(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        work = Work.objects.create(cv=cv, name='Daily Bugle', position='Reporter',
                                   start_date=datetime.date(2000, 1, 1),
                                   end_date=datetime.date(1337, 1, 1))
        project = Project.objects.create(cv=cv,
                                         work=work,
                                         name='Expose Luthor',
                                         description="Find and report misdeeds by Luthor",
                                         type='article',
                                         start_date=datetime.date(1990, 1, 1),
                                         end_date=datetime.date(2000, 1, 1))
        self.assertEqual(work.project_set.count(), 1)
        self.assertEqual(work.project_set.first(), project)
        self.assertEqual(cv.project_set.count(), 1)
        self.assertEqual(cv.work_projects.count(), 1)
        self.assertEqual(cv.work_projects[0], project)
        self.assertEqual(cv.hobby_projects.count(), 0)


class EducationModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        education = Education(cv=cv, institution='University of Oklahoma', area="IT", study_type='Bachelor', gpa='4.0',
                              start_date=datetime.date(2011, 6, 1),
                              end_date=datetime.date(2014, 1, 1))
        education.save()
        self.assertEqual(Education.objects.all().count(), 1)
        self.assertEqual(Education.objects.all()[0], education)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        education = Education.objects.create(cv=cv, institution='University of Oklahoma', area="IT",
                                             study_type='Bachelor', gpa='4.0',
                                             start_date=datetime.date(2011, 6, 1),
                                             end_date=datetime.date(2014, 1, 1))
        self.assertEqual(str(education), '{}:{}:{}'.format(education.institution, education.area, education.study_type))

    def test_duration(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        education = Education.objects.create(cv=cv, institution='University of Oklahoma', area="IT",
                                             study_type='Bachelor', gpa='4.0',
                                             start_date=datetime.date(2011, 6, 1),
                                             end_date=datetime.date(2014, 1, 1))
        self.assertEqual(education.duration_years, 2)
        self.assertEqual(education.duration_months, 7)
        self.assertEqual(education.duration_str, '2 years, 7 months')


class ProjectModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        project = Project(cv=cv, name='Miss Direction', description="A mapping engine that misguides you",
                          type='application',
                          keywords='["GoogleMaps", "JavaScript"]',
                          industry='Consumer',
                          client='Navigore',
                          start_date=datetime.date(2016, 8, 24),
                          end_date=datetime.date(2016, 8, 24))
        project.save()
        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(Project.objects.all()[0], project)
        self.assertEqual(cv.hobby_projects.count(), 1)
        self.assertEqual(cv.hobby_projects[0], project)
        self.assertEqual(cv.work_projects.count(), 0)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        project = Project.objects.create(cv=cv, name='Miss Direction',
                                         description="A mapping engine that misguides you",
                                         type='application',
                                         start_date=datetime.date(2016, 8, 24),
                                         end_date=datetime.date(2016, 8, 24))
        self.assertEqual(str(project), project.name)
        self.assertEqual(project.duration_str, '')

    def test_keyword_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        project = Project.objects.create(cv=cv, name='Miss Direction',
                                         description="A mapping engine that misguides you",
                                         type='application',
                                         keywords='["GoogleMaps", "JavaScript"]',
                                         start_date=datetime.date(2016, 8, 24),
                                         end_date=datetime.date(2016, 8, 24))
        self.assertEqual(str(project), project.name)
        self.assertEqual(project.duration_str, '')
        self.assertEqual(project.keyword_str, 'GoogleMaps, JavaScript')

    def test_duration(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        project = Project.objects.create(cv=cv, name='Miss Direction',
                                         description="A mapping engine that misguides you",
                                         type='application',
                                         start_date=datetime.date(2016, 8, 1),
                                         end_date=datetime.date(2016, 9, 1))
        self.assertEqual(project.duration_str, '1 month')
        self.assertEqual(project.duration_years, 0)
        self.assertEqual(project.duration_months, 1)

    def test_duration_with_no_end_date(self):
        """ Using date 1337-01-01 should cause it to be replaced by current date in duration calculations """
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        project = Project.objects.create(cv=cv, name='Miss Direction',
                                         description="A mapping engine that misguides you",
                                         type='application',
                                         start_date=datetime.date(2000, 1, 1),
                                         end_date=datetime.date(1337, 1, 1))
        today = datetime.date.today()
        self.assertEqual(project.duration_years, today.year - project.start_date.year)
        self.assertEqual(project.duration_months, today.month - project.start_date.month)


class SkillModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        skill = Skill(cv=cv, name='Compression', level='Master', keywords='["MPEG","MP4","GIF"]')
        skill.save()
        self.assertEqual(Skill.objects.all().count(), 1)
        self.assertEqual(Skill.objects.all()[0], skill)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        skill = Skill.objects.create(cv=cv, name='Compression', level='Master', keywords='["MPEG","MP4","GIF"]')
        self.assertEqual(str(skill), '{}:{}'.format(skill.name, skill.level))


class LanguageModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        language = Language(cv=cv, name='English', fluency='Native')
        language.save()
        self.assertEqual(Language.objects.all().count(), 1)
        self.assertEqual(Language.objects.all()[0], language)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        language = Language.objects.create(cv=cv, name='English', fluency='Native')
        self.assertEqual(str(language), '{}:{}'.format(language.name, language.fluency))


class VolunteerModelTest(TestCase):
    def test_can_save_and_load(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        volunteer = Volunteer(cv=cv, organization='CoderDojo', position="Teacher",
                              url='http://coderdojo.example.com/',
                              summary='Global movement of free coding clubs for young people.',
                              start_date=datetime.date(2012, 1, 1),
                              end_date=datetime.date(2013, 1, 1))
        volunteer.save()
        self.assertEqual(Volunteer.objects.all().count(), 1)
        self.assertEqual(Volunteer.objects.all()[0], volunteer)

    def test_string(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        volunteer = Volunteer.objects.create(cv=cv, organization='CoderDojo', position="Teacher",
                                             url='http://coderdojo.example.com/',
                                             summary='Global movement of free coding clubs for young people.',
                                             start_date=datetime.date(2012, 1, 1),
                                             end_date=datetime.date(2013, 1, 1))
        self.assertEqual(str(volunteer), '{}:{}'.format(volunteer.organization, volunteer.position))

    def test_duration(self):
        user = auth.get_user_model().objects.create(username='creator')
        cv = Cv.objects.create(user=user, name='cv', title='CV')
        volunteer = Volunteer.objects.create(cv=cv, organization='CoderDojo', position="Teacher",
                                             url='http://coderdojo.example.com/',
                                             summary='Global movement of free coding clubs for young people.',
                                             start_date=datetime.date(2012, 1, 1),
                                             end_date=datetime.date(2013, 1, 1))
        self.assertEqual(volunteer.duration_str, '1 year')
        self.assertEqual(volunteer.duration_years, 1)
        self.assertEqual(volunteer.duration_months, 0)
