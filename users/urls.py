from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CvUserList, CvUserDetail, CvUserUpdate, CvUserDelete


urlpatterns = [
    path("user/<slug:slug>/edit/", login_required(CvUserUpdate.as_view()), name='user_update'),
    path("user/<slug:slug>/delete/", login_required(CvUserDelete.as_view()), name='user_delete'),
    path("user/<slug:slug>/", CvUserDetail.as_view(), name='user_detail'),
    path("users/", login_required(CvUserList.as_view()), name='user_list'),
    path("accounts/profile/", login_required(CvUserDetail.as_view()), name='profile'),
]
