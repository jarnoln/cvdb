from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib import auth


class HomeView(TemplateView):
    template_name = 'viewcv/home.html'


class ProfileView(DetailView):
    template_name = 'viewcv/profile.html'

    def get_object(self, queryset=None):
        return auth.get_user(self.request)


class CvUserDelete(DeleteView):
    slug_field = 'username'
    model = auth.models.User
    success_url = reverse_lazy('home')

    def render_to_response(self, context, **response_kwargs):
        return super(CvUserDelete, self).render_to_response(context, **response_kwargs)
