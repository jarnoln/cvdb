from django.db import models
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.utils.translation import ugettext_lazy


class Cv(models.Model):
    user = models.ForeignKey(auth.get_user_model(), null=True, blank=True, default=None)
    name = models.SlugField(max_length=100, default='default', verbose_name=ugettext_lazy('name'),
                            help_text=ugettext_lazy('Must be unique. Used in URL.'))
    title = models.CharField(max_length=250, blank=True, default='', verbose_name=ugettext_lazy('title'))
    summary = models.TextField(blank=True, default='')

    def can_edit(self, user):
        return user == self.user

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('cv', args=[self.id])


class Work(models.Model):
    cv = models.ForeignKey(Cv, null=True, blank=True, default=None)
    company = models.CharField(max_length=250, blank=True, default='')
    position = models.CharField(max_length=250, blank=True, default='')
    website = models.URLField(max_length=250, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True, default='')

    @property
    def duration(self):
        years = self.end_date.year - self.start_date.year
        months = self.end_date.month - self.start_date.month
        if months < 0:
            years = years - 1
            months = months + 12
        return years, months

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
        duration_y = ''
        duration_m = ''
        if years > 1:
            duration_y = '{} years'.format(years)
        elif years == 1:
            duration_y = '1 year'
        if months > 1:
            duration_m = '{} months'.format(months)
        elif months == 1:
            duration_m = '1 month'
        if duration_y and duration_m:
            return '{}, {}'.format(duration_y, duration_m)

        return duration_y + duration_m

    def __str__(self):
        return '{}:{}'.format(self.company, self.position)

    class Meta:
        ordering = ['-start_date']
