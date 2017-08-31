from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from .views import submit_resume


router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^resume/', login_required(submit_resume), name='submit_resume'),
]
