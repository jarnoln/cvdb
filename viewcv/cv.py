import weasyprint
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import Http404, HttpResponse
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import Cv


class CvOwnList(ListView):
    model = Cv

    def get_queryset(self):
        # Only list own CVs
        return Cv.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CvOwnList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvPublicList(ListView):
    model = Cv
    template_name = 'viewcv/cv_public_list.html'

    def get_queryset(self):
        # Only list public CVs
        return Cv.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super(CvPublicList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvDetail(DetailView):
    model = Cv

    def get_object(self, queryset=None):
        if 'slug' in self.kwargs:
            user = get_object_or_404(auth.get_user_model(), username=self.kwargs['slug'])
            cv = Cv.objects.filter(user=user, public=True, primary=True)
            if cv.count() == 0:
                raise Http404
            elif cv.count() == 1:
                return cv.first()
            else:
                return cv.first()
        else:
            return super(CvDetail, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(CvDetail, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        context['display'] = self.request.GET.get('display', '')
        context['format'] = self.request.GET.get('format', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if context['format'] == 'pdf':
            file_name = '{}.pdf'.format(self.object.user.username)
            html_string = render_to_string(self.get_template_names()[0], context=context)
            html = weasyprint.HTML(string=html_string)
            html.write_pdf(file_name)
            # fs = FileSystemStorage('/tmp')
            with open(file_name, 'rb') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
                return response

        return super(CvDetail, self).render_to_response(context, **response_kwargs)


class CvUpdate(UpdateView):
    model = Cv
    fields = ['name', 'title', 'summary', 'public', 'primary']

    def get_object(self):
        cv = super(CvUpdate, self).get_object()
        if cv.can_edit(self.request.user):
            return cv

        # Todo: Smarter way to handle this
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(CvUpdate, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message', '')
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('cv', args=[self.object.id])
        else:
            return reverse('cv_list')


class CvDelete(DeleteView):
    model = Cv
    success_url = reverse_lazy('cv_list')

    def get_object(self):
        cv = super(CvDelete, self).get_object()
        if cv.can_edit(self.request.user):
            return cv

        # Todo: Smarter way to handle this
        raise Http404

    def render_to_response(self, context, **response_kwargs):
        return super(CvDelete, self).render_to_response(context, **response_kwargs)
