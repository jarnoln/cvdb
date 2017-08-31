from django.conf.urls import url
from .views import HomeView, UploadCvView


urlpatterns = [
    url(r'^upload/$', UploadCvView.as_view(), name='upload'),
    url(r'^$', HomeView.as_view(), name='home'),
]
