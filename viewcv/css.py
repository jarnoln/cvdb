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


class CssUpdate(UpdateView):
    model = Css
    fields = ['name', 'title', 'css']

    def get_object(self):
        css = super(CssUpdate, self).get_object()
        if css.can_edit(self.request.user):
            return css

        # Todo: Smarter way to handle this
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(CssUpdate, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message', '')
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('css_update', args=[self.object.id])
        else:
            return reverse('css_list')
