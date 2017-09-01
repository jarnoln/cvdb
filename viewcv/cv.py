from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import Http404
from django.contrib import auth
from .models import Cv


class CvList(ListView):
    model = Cv

    def get_context_data(self, **kwargs):
        context = super(CvList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvDetail(DetailView):
    model = Cv

    # def get_object(self, queryset=None):
    #    target_username = self.kwargs.get('slug', '')
    #    if target_username:
    #        # return auth.models.User.objects.get(username=target_username)
    #        return auth.get_user_model().objects.get(username=target_username)
    #    return auth.get_user(self.request)


class CvUpdate(UpdateView):
    model = auth.get_user_model()
    fields = ['summary']

    def get_object(self):
        target_user = super(CvUpdate, self).get_object()
        if can_edit_user(logged_user=self.request.user, target_user=target_user):
            return target_user

        # Todo: Smarter way to handle this
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(CvUpdate, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message', '')
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('user_detail', args=[self.object.username])
        else:
            return reverse('user_list')


class CvDelete(DeleteView):
    model = Cv
    success_url = reverse_lazy('cv_list')

    def get_object(self):
        cv = super(CvDelete, self).get_object()
        if cv.user == self.request.user:
            return cv

        # Todo: Smarter way to handle this
        raise Http404

    def render_to_response(self, context, **response_kwargs):
        return super(CvDelete, self).render_to_response(context, **response_kwargs)
