import logging
import weasyprint
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import Http404, HttpResponse
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import Css


class CssList(ListView):
    model = Css
    template_name = 'viewcv/css_list.html'

    def get_queryset(self):
        return Css.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CssList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context
