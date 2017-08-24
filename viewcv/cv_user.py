from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import DeleteView
from django.http import Http404
from django.contrib import auth


def can_edit_user(logged_user, target_user):
    """ Is logged in user allowed to edit target user """
    if logged_user == target_user:
        return True
    if logged_user.is_staff:
        return True
    return False


class ProfileView(DetailView):
    template_name = 'viewcv/profile.html'
    context_object_name = 'target_user'

    def get_object(self, queryset=None):
        target_username = self.kwargs.get('slug', '')
        if target_username:
            # return auth.models.User.objects.get(username=target_username)
            return auth.get_user_model().objects.get(username=target_username)
        return auth.get_user(self.request)


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
