from django.conf.urls import include, url
from rest_framework import routers
from .views import submit_resume


router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^resume/', submit_resume, name='submit_resume'),
]
