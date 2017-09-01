from django.conf.urls import url
from .views import HomeView, UploadCvView
from .cv import CvList


urlpatterns = [
    url(r'^upload/$', UploadCvView.as_view(), name='upload'),
    url(r'^cvs/$', CvList.as_view(), name='cv_list'),
    url(r'^$', UploadCvView.as_view(), name='home'),
]
