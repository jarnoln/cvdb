from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .views import submit_resume, submit_resume_file


app_name = 'api01'
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^submit_resume_file/', login_required(submit_resume_file), name='submit_resume_file'),
    url(r'^resume/', login_required(submit_resume), name='submit_resume'),
]
