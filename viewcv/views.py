from django import forms
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


class HomeView(TemplateView):
    template_name = 'viewcv/home.html'


class UploadForm(forms.Form):
    json_file = forms.FileField()


class UploadCvView(FormView):
    template_name = 'viewcv/upload.html'
    form_class = UploadForm
    success_url = '/'

    # def form_valid(self, form):
    #    print('form_valid')
    #    uploaded_file = self.request.FILES['file']
    #    print('Uploaded file:' + uploaded_file)
    #    return super(UploadCvView, self).form_valid(form)
