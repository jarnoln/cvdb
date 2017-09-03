import json
from django import forms
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from api01.views import create_resume


class UploadForm(forms.Form):
    json_file = forms.FileField(label='Resume')


class HomeView(FormView):
    template_name = 'viewcv/home.html'
    form_class = UploadForm


class UploadCvView(FormView):
    template_name = 'viewcv/upload.html'
    form_class = UploadForm
    cv_id = 0

    def form_valid(self, form):
        # print('form_valid')
        resume_file = self.request.FILES['json_file']
        # print('resume file=%s' % resume_file)
        file_content = resume_file.read()
        data = json.loads(file_content.decode('utf-8'))
        response = create_resume(data, self.request.user)
        response_data = json.loads(response.content.decode('utf-8'))
        self.cv_id = response_data['id']
        return super(UploadCvView, self).form_valid(form)

    def get_success_url(self):
        if self.cv_id:
            return reverse_lazy('cv', args=[self.cv_id])
        else:
            return reverse('home')
