from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .upload import UploadCvView
from .about import AboutView
from .cv import CvOwnList, CvPublicList, CvDetail, CvUpdate, CvDelete


urlpatterns = [
    url(r'^u/(?P<slug>\w+)/$', CvDetail.as_view(), name='cv_public'),
    url(r'^cv/(?P<pk>\d+)/edit/$', login_required(CvUpdate.as_view()), name='cv_update'),
    url(r'^cv/(?P<pk>\d+)/delete/$', login_required(CvDelete.as_view()), name='cv_delete'),
    url(r'^cv/(?P<pk>\d+)/$', login_required(CvDetail.as_view()), name='cv'),
    url(r'^upload/$', login_required(UploadCvView.as_view()), name='upload'),
    url(r'^list/$', CvPublicList.as_view(), name='cv_public_list'),
    url(r'^my_cvs/$', login_required(CvOwnList.as_view()), name='cv_list'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^$', UploadCvView.as_view(), name='home'),
]
