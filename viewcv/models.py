from django.db import models
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.utils.translation import ugettext_lazy
from viewcv.durations import calculate_duration, duration_as_string


class Cv(models.Model):
    user = models.ForeignKey(auth.get_user_model(), null=True, blank=True, default=None)
    name = models.SlugField(max_length=100, default='default', verbose_name=ugettext_lazy('name'),
                            help_text=ugettext_lazy('Must be unique. Used in URL.'))
    title = models.CharField(max_length=250, blank=True, default='', verbose_name=ugettext_lazy('title'))
    summary = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    edited = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def personal(self):
        personal = Personal.objects.filter(cv=self)
        if personal.count() == 1:
            return personal.first()
        return None

    def can_edit(self, user):
        return user == self.user

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('cv', args=[self.id])


class Personal(models.Model):
    cv = models.ForeignKey(Cv, null=True, blank=True, default=None)
    email = models.EmailField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    image = models.URLField(max_length=250, blank=True, default='')
    summary = models.TextField(blank=True, default='')


class Work(models.Model):
    cv = models.ForeignKey(Cv, null=True, blank=True, default=None)
    name = models.CharField(max_length=250, blank=True, default='')
    position = models.CharField(max_length=250, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True, default='')

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
        return '{}:{}'.format(self.name, self.position)

    class Meta:
        ordering = ['-end_date']


class Education(models.Model):
    cv = models.ForeignKey(Cv, null=True, blank=True, default=None)
    institution = models.CharField(max_length=250, blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    area = models.CharField(max_length=250, blank=True, default='')
    study_type = models.CharField(max_length=250, blank=True, default='')
    gpa = models.CharField(max_length=50, blank=True, default='')
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
        return '{}:{}:{}'.format(self.institution, self.area, self.study_type)

    class Meta:
        ordering = ['-end_date']


class Project(models.Model):
    cv = models.ForeignKey(Cv, null=True, blank=True, default=None)
    name = models.CharField(max_length=250, blank=True, default='')
    description = models.TextField(blank=True, default='')
    url = models.URLField(max_length=250, blank=True, default='')
    keywords = models.CharField(max_length=250, blank=True, default='[]')  # Actually a list
    roles = models.CharField(max_length=250, blank=True, default='[]')  # Actually a list
    entity = models.CharField(max_length=250, blank=True, default='')
    type = models.CharField(max_length=250, blank=True, default='')
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
        return '{}'.format(self.name)

    class Meta:
        ordering = ['-end_date']
