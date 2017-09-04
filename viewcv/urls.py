from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import HomeView, UploadCvView
from .cv import CvList, CvDetail, CvUpdate, CvDelete


urlpatterns = [
    url(r'^u/(?P<slug>\w+)/cv/$', CvDetail.as_view(), name='cv_public'),
    url(r'^cv/(?P<pk>\d+)/edit/$', login_required(CvUpdate.as_view()), name='cv_update'),
    url(r'^cv/(?P<pk>\d+)/delete/$', login_required(CvDelete.as_view()), name='cv_delete'),
    url(r'^cv/(?P<pk>\d+)/$', login_required(CvDetail.as_view()), name='cv'),
    url(r'^upload/$', login_required(UploadCvView.as_view()), name='upload'),
    url(r'^cvs/$', login_required(CvList.as_view()), name='cv_list'),
    url(r'^$', UploadCvView.as_view(), name='home'),
]
