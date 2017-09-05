from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import Http404
from django.contrib import auth
from django.shortcuts import get_object_or_404
from .models import Cv


class CvOwnList(ListView):
    model = Cv

    def get_queryset(self):
        # Only list own CVs
        return Cv.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CvOwnList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvPublicList(ListView):
    model = Cv
    template_name = 'viewcv/cv_public_list.html'

    def get_queryset(self):
        # Only list public CVs
        return Cv.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super(CvPublicList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvDetail(DetailView):
    model = Cv

    def get_object(self, queryset=None):
        if 'slug' in self.kwargs:
            user = get_object_or_404(auth.get_user_model(), username=self.kwargs['slug'])
            cv = Cv.objects.filter(user=user, public=True, primary=True)
            if cv.count() == 0:
                raise Http404
            elif cv.count() == 1:
                return cv.first()
            else:
                return cv.first()
        else:
            return super(CvDetail, self).get_object()


class CvUpdate(UpdateView):
    model = Cv
    fields = ['name', 'title', 'summary', 'public', 'primary']

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
