from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'viewcv/home.html'


class UploadCvView(TemplateView):
    template_name = 'viewcv/upload.html'
