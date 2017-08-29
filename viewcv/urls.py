from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .cv_user import CvUserList, CvUserDetail, CvUserDelete
from .views import HomeView


urlpatterns = [
    url(r'^user/(?P<slug>[\w\.-]+)/delete/$', login_required(CvUserDelete.as_view()), name='user_delete'),
    url(r'^user/(?P<slug>[\w\.-]+)/$', CvUserDetail.as_view(), name='user_detail'),
    url(r'^users/$', login_required(CvUserList.as_view()), name='user_list'),
    url(r'^accounts/profile/$', login_required(CvUserDetail.as_view()), name='profile'),
    url(r'^$', HomeView.as_view(), name='home'),
]
