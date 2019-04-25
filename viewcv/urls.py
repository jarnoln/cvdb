from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .upload import UploadCvView, UploadCssView
from .about import AboutView
from .cv import CvOwnList, CvPublicList, CvDetail, CvUpdate, CvDelete
from .css import CssList, CssUpdate, CssDelete


urlpatterns = [
    url(r'^u/(?P<slug>\w+)/$', CvDetail.as_view(), name='cv_public'),
    url(r'^css/(?P<pk>\d+)/edit/$', login_required(CssUpdate.as_view()), name='css_update'),
    url(r'^css/(?P<pk>\d+)/delete/$', login_required(CssDelete.as_view()), name='css_delete'),
    url(r'^cv/(?P<pk>\d+)/edit/$', login_required(CvUpdate.as_view()), name='cv_update'),
    url(r'^cv/(?P<pk>\d+)/delete/$', login_required(CvDelete.as_view()), name='cv_delete'),
    url(r'^cv/(?P<pk>\d+)/$', login_required(CvDetail.as_view()), name='cv'),
    url(r'^upload-css/$', login_required(UploadCssView.as_view()), name='upload_css'),
    url(r'^upload/$', login_required(UploadCvView.as_view()), name='upload'),
    url(r'^css_list/$', CssList.as_view(), name='css_list'),
    url(r'^list/$', CvPublicList.as_view(), name='cv_public_list'),
    url(r'^my_cvs/$', login_required(CvOwnList.as_view()), name='cv_list'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^$', UploadCvView.as_view(), name='home'),
]
