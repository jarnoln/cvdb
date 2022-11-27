from django.urls import include, path
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .views import submit_resume, submit_resume_file


app_name = 'api01'
router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("submit_resume_file/", login_required(submit_resume_file), name='submit_resume_file'),
    path("resume/", login_required(submit_resume), name='submit_resume'),
]
