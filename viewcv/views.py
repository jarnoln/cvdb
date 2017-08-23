from django.views.generic import TemplateView, DetailView
from django.contrib import auth


class HomeView(TemplateView):
    template_name = 'viewcv/home.html'


class ProfileView(DetailView):
    template_name = 'viewcv/profile.html'

    def get_object(self, queryset=None):
        return auth.get_user(self.request)
