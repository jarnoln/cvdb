# from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from .upload import UploadCvView, UploadCssView
from .about import AboutView
from .cv import CvOwnList, CvPublicList, CvDetail, CvUpdate, CvSetAsPrimary, CvDelete
from .css import CssList, CssUpdate, CssDelete


urlpatterns = [
    path("u/<slug:username>/", CvDetail.as_view(), name='cv_public'),
    path("css/<int:pk>/edit/", login_required(CssUpdate.as_view()), name='css_update'),
    path("css/<int:pk>/delete/", login_required(CssDelete.as_view()), name='css_delete'),
    path("cv/<int:pk>/set_as_primary/", login_required(CvSetAsPrimary.as_view()), name='cv_set_as_primary'),
    path("cv/<int:pk>/edit/", login_required(CvUpdate.as_view()), name='cv_update'),
    path("cv/<int:pk>/delete/", login_required(CvDelete.as_view()), name='cv_delete'),
    path("cv/<int:pk>/", login_required(CvDetail.as_view()), name='cv'),
    path("upload-css/", login_required(UploadCssView.as_view()), name='upload_css'),
    path("upload/", login_required(UploadCvView.as_view()), name='upload'),
    path("css_list/", CssList.as_view(), name='css_list'),
    path("list/", CvPublicList.as_view(), name='cv_public_list'),
    path("my_cvs/", login_required(CvOwnList.as_view()), name='cv_list'),
    path("about/", AboutView.as_view(), name='about'),
    path("", UploadCvView.as_view(), name='home'),
]
