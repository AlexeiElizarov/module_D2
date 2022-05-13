from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProfileForm, BaseRegisterForm
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create-дженерик для формы создания нового пользователя
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class CreateProfilePageView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'sign/create_profile.html'
    fields = ['about', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('create_user_profile')   # FIXME


class UpdateProfilePageView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'sign/edit_profile.html'
    success_url = reverse_lazy('user_profile_page')

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.request.user.id
        return Profile.objects.get(user_id=id)


class GetProfileMixin(object):
    def get_object(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        if profile.user != self.request.user:
            raise Http404
        return profile


class ShowProfilePageView(LoginRequiredMixin, GetProfileMixin, DetailView):
    model = Profile
    template_name = 'sign/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, user_id=self.request.user.id)
        context['page_user'] = page_user
        return context
