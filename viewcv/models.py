from django.db import models
from django.contrib import auth
from django.utils.translation import ugettext_lazy


class Cv(models.Model):
    user = models.ForeignKey(auth.get_user_model(), null=True, blank=True, default=None)
    name = models.SlugField(max_length=100, unique=True, verbose_name=ugettext_lazy('name'),
                            help_text=ugettext_lazy('Must be unique. Used in URL.'))
    title = models.CharField(max_length=250, blank=True, default='', verbose_name=ugettext_lazy('title'))

    def __str__(self):
        return '{}'.format(self.name)


class Work(models.Model):
    cv = models.ForeignKey(Cv, null=True, blank=True, default=None)
    company = models.CharField(max_length=250, blank=True, default='')
    position = models.CharField(max_length=250, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True, default='')

    def __str__(self):
        return '{}:{}'.format(self.company, self.position)
