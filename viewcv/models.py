import json
import datetime
from django.db import models
from django.urls import reverse
from django.contrib import auth
from django.utils.translation import ugettext_lazy
from viewcv.durations import calculate_duration, duration_as_string


class Css(models.Model):
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.SlugField(max_length=100, default='', verbose_name=ugettext_lazy('name'))
    title = models.CharField(max_length=250, blank=True, default='', verbose_name=ugettext_lazy('title'))
    summary = models.TextField(blank=True, default='')
    css = models.TextField(blank=True, default='')

    def can_edit(self, user):
        return user == self.creator

    def __str__(self):
        return self.title
        # return '{}:{}'.format(self.name, self.title)


class CssUrl(models.Model):
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.SlugField(max_length=100, default='bootstrap400', verbose_name=ugettext_lazy('name'))
    title = models.CharField(max_length=250, blank=True, default='Bootstrap 4.0.0', verbose_name=ugettext_lazy('title'))
    summary = models.TextField(blank=True, default='')
    url = models.URLField(max_length=250, blank=True,
                          help_text=ugettext_lazy('Link to CSS file'),
                          default='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css')

    def __str__(self):
        return self.title
        # return '{}:{}:{}'.format(self.name, self.title, self.url)


class Cv(models.Model):
    user = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.SlugField(max_length=100, default='default', verbose_name=ugettext_lazy('name'))
    title = models.CharField(max_length=250, blank=True, default='', verbose_name=ugettext_lazy('title'))
    summary = models.TextField(blank=True, default='')
    public = models.BooleanField(blank=True, default=False,
                                 help_text=ugettext_lazy('Are other users allowed to see this CV'))
    primary = models.BooleanField(blank=True, default=False,
                                  help_text=ugettext_lazy('Is this the primary CV for this user'))
    css = models.ForeignKey(Css, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                            help_text=ugettext_lazy('CSS used for styling CV'))
    css_url = models.ForeignKey(CssUrl, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                help_text=ugettext_lazy('Link to CSS file used for styling CV'))
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def personal(self):
        personal = Personal.objects.filter(cv=self)
        if personal.count() == 1:
            return personal.first()
        return None

    @property
    def specialties(self):
        return Skill.objects.filter(cv=self, level='Excellent')

    @property
    def non_specialties(self):
        return Skill.objects.filter(cv=self).exclude(level='Excellent')

    @property
    def hobby_projects(self):
        return Project.objects.filter(cv=self, work=None)

    @property
    def work_projects(self):
        return Project.objects.filter(cv=self).exclude(work=None)

    def can_edit(self, user):
        return user == self.user

    def set_as_primary(self):
        # First make all CVs non-primary, then set this one as primary (so there is only one primary CV)
        if not self.primary:
            Cv.objects.filter(user=self.user).update(primary=False)
            self.primary = True
            self.public = True
            self.save()

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('cv', args=[self.id])

    class Meta:
        ordering = ['-created']


class Personal(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    email = models.EmailField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    image = models.URLField(max_length=250, blank=True, default='')
    profiles = models.CharField(max_length=1000, blank=True, default='[]')  # Actually a list
    summary = models.TextField(blank=True, default='')

    @property
    def profile_list(self):
        return json.loads(self.profiles)


class Work(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=250, blank=True, default='')
    position = models.CharField(max_length=250, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True, default='')

    @property
    def end_date_current(self):  # Replaces end date with current date if not defined
        if self.end_date.year == 1337:
            return datetime.datetime.now()
        return self.end_date

    @property
    def duration(self):
        if self.end_date.year == 1337:
            return calculate_duration(self.start_date, None)
        return calculate_duration(self.start_date, self.end_date)

    @property
    def duration_years(self):
        years, months = self.duration
        return years

    @property
    def duration_months(self):
        years, months = self.duration
        return months

    @property
    def duration_str(self):
        years, months = self.duration
        return duration_as_string(years, months)

    def __str__(self):
        return '{}:{}'.format(self.name, self.position)

    class Meta:
        ordering = ['-start_date']


class Education(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    institution = models.CharField(max_length=250, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    area = models.CharField(max_length=250, blank=True, default='')
    study_type = models.CharField(max_length=250, blank=True, default='')
    gpa = models.CharField(max_length=50, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    @property
    def end_date_current(self):  # Replaces end date with current date if not defined
        if self.end_date.year == 1337:
            return datetime.datetime.now()
        return self.end_date

    @property
    def duration(self):
        if self.end_date.year == 1337:
            return calculate_duration(self.start_date, None)
        return calculate_duration(self.start_date, self.end_date)

    @property
    def duration_years(self):
        years, months = self.duration
        return years

    @property
    def duration_months(self):
        years, months = self.duration
        return months

    @property
    def duration_str(self):
        years, months = self.duration
        return duration_as_string(years, months)

    def __str__(self):
        return '{}:{}:{}'.format(self.institution, self.area, self.study_type)

    class Meta:
        ordering = ['-end_date']


class Volunteer(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    organization = models.CharField(max_length=250, blank=True, default='')
    position = models.CharField(max_length=250, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    @property
    def duration(self):
        return calculate_duration(self.start_date, self.end_date)

    @property
    def duration_years(self):
        years, months = self.duration
        return years

    @property
    def duration_months(self):
        years, months = self.duration
        return months

    @property
    def duration_str(self):
        years, months = self.duration
        return duration_as_string(years, months)

    def __str__(self):
        return '{}:{}'.format(self.organization, self.position)

    class Meta:
        ordering = ['-end_date']


class Skill(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=250, blank=True, default='')
    level = models.CharField(max_length=100, blank=True, default='')
    keywords = models.CharField(max_length=500, blank=True, default='[]')  # Actually a list

    def __str__(self):
        return '{}:{}'.format(self.name, self.level)

    class Meta:
        ordering = ['name']


class Language(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=250, blank=True, default='')
    fluency = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return '{}:{}'.format(self.name, self.fluency)


class Project(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # If this project was a work project, can add link here
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField(blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    keywords = models.CharField(max_length=250, blank=True, default='[]')  # Actually a list
    roles = models.CharField(max_length=250, blank=True, default='[]')  # Actually a list
    entity = models.CharField(max_length=250, blank=True, default='')
    type = models.CharField(max_length=250, blank=True, default='')
    industry = models.CharField(max_length=250, blank=True, default='')
    client = models.CharField(max_length=250, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    @property
    def end_date_current(self):  # Replaces end date with current date if not defined
        if self.end_date.year == 1337:
            return datetime.datetime.now()
        return self.end_date

    @property
    def duration(self):
        if self.end_date.year == 1337:
            return calculate_duration(self.start_date, None)
        return calculate_duration(self.start_date, self.end_date)

    @property
    def duration_years(self):
        years, months = self.duration
        return years

    @property
    def duration_months(self):
        years, months = self.duration
        return months

    @property
    def duration_str(self):
        years, months = self.duration
        return duration_as_string(years, months)

    @property
    def keyword_str(self):
        keywords = json.loads(self.keywords)
        return ', '.join(keywords)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['-start_date']
