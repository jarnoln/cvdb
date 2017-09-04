from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import Http404
from django.contrib import auth
from .models import Cv


class CvList(ListView):
    model = Cv

    def get_queryset(self):
        # Only list own CVs
        return Cv.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CvList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvDetail(DetailView):
    model = Cv


class CvUpdate(UpdateView):
    model = Cv
    fields = ['name', 'title', 'summary']

    def get_object(self):
        cv = super(CvUpdate, self).get_object()
        if cv.can_edit(self.request.user):
            return cv

        # Todo: Smarter way to handle this
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(CvUpdate, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message', '')
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('cv', args=[self.object.id])
        else:
            return reverse('cv_list')


class CvDelete(DeleteView):
    model = Cv
    success_url = reverse_lazy('cv_list')

    def get_object(self):
        cv = super(CvDelete, self).get_object()
        if cv.can_edit(self.request.user):
            return cv

        # Todo: Smarter way to handle this
        raise Http404

    def render_to_response(self, context, **response_kwargs):
        return super(CvDelete, self).render_to_response(context, **response_kwargs)
