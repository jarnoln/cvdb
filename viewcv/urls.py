from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import HomeView, ProfileView, CvUserDelete

urlpatterns = [
    url(r'^user/(?P<slug>[\w\.-]+)/delete/$', login_required(CvUserDelete.as_view()), name='user_delete'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^$', HomeView.as_view(), name='home'),
]
