from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import Http404
from django.contrib import auth


def can_edit_user(logged_user, target_user):
    """ Is logged in user allowed to edit target user """
    if logged_user == target_user:
        return True
    if logged_user.is_staff:
        return True
    return False


class CvUserList(ListView):
    model = auth.get_user_model()

    def get_context_data(self, **kwargs):
        context = super(CvUserList, self).get_context_data(**kwargs)
        context['messages'] = self.request.GET.get('message', '')
        return context


class CvUserDetail(DetailView):
    template_name = 'viewcv/profile.html'
    context_object_name = 'target_user'

    def get_object(self, queryset=None):
        target_username = self.kwargs.get('slug', '')
        if target_username:
            # return auth.models.User.objects.get(username=target_username)
            return auth.get_user_model().objects.get(username=target_username)
        return auth.get_user(self.request)


class CvUserUpdate(UpdateView):
    model = auth.get_user_model()
    slug_field = 'username'
    fields = ['first_name', 'last_name']

    def get_object(self):
        target_user = super(CvUserUpdate, self).get_object()
        if can_edit_user(logged_user=self.request.user, target_user=target_user):
            return target_user

        # Todo: Smarter way to handle this
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(CvUserUpdate, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message', '')
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('user_detail', args=[self.object.username])
        else:
            return reverse('user_list')


class CvUserDelete(DeleteView):
    slug_field = 'username'
    model = auth.models.User
    success_url = reverse_lazy('home')

    def get_object(self):
        target_user = super(CvUserDelete, self).get_object()
        if can_edit_user(logged_user=self.request.user, target_user=target_user):
            return target_user

        # Todo: Smarter way to handle this
        raise Http404

    def render_to_response(self, context, **response_kwargs):
        return super(CvUserDelete, self).render_to_response(context, **response_kwargs)
