from django.conf.urls import url
from .views import HomeView, ProfileView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
]
