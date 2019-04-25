import json
from django import forms
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from api01.views import create_resume
from viewcv.models import Css


class UploadCvForm(forms.Form):
    json_file = forms.FileField(label='Select CV/Resume file to upload')


class UploadCssForm(forms.Form):
    css_file = forms.FileField(label='Select CSS file to upload')


class UploadCvView(FormView):
    template_name = 'viewcv/upload.html'
    form_class = UploadCvForm
    cv_id = 0

    def form_valid(self, form):
        resume_file = self.request.FILES['json_file']
        file_content = resume_file.read()
        data = json.loads(file_content.decode('utf-8'))
        response = create_resume(data, self.request.user)
        response_data = json.loads(response.content.decode('utf-8'))
        # print(response_data)
        self.cv_id = response_data['id']
        return super(UploadCvView, self).form_valid(form)

    def get_success_url(self):
        if self.cv_id:
            return reverse_lazy('cv', args=[self.cv_id])
        else:
            return reverse('home')


class UploadCssView(FormView):
    template_name = 'viewcv/upload_css.html'
    form_class = UploadCssForm
    css_id = 0

    def form_valid(self, form):
        css_file = self.request.FILES['css_file']
        file_content = css_file.read()
        # data = json.loads(file_content.decode('utf-8'))
        # response = create_resume(data, self.request.user)
        css = Css.objects.create(creator=self.request.user, name='default', css=file_content.decode('UTF-8'))
        self.css_id = css.id
        return super(UploadCssView, self).form_valid(form)

    def get_success_url(self):
        if self.css_id:
            return reverse_lazy('css_update', args=[self.css_id])
        else:
            return reverse('css_list')
