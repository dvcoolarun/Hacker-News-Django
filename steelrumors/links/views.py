from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth import get_user_model
from .models import Link, Vote, UserProfile

from django.shortcuts import render
from django.views import generic

from .forms import UserProfileForm, LinkForm
from django.core.urlresolvers import reverse


class LinkListView(generic.ListView):
    model = Link
    queryset = Link.with_votes.all()
    paginate_by = 3


class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user


# For Editing your Profile Details
class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


class LinkCreateView(CreateView):
    model = Link
    form_class = LinkForm

    def form_valid(self, form):
        # Firstly Because of CreateView First
        # of all you have to save form to get an object.

        # Do not persisting object to database for further
        # customization(commit=False)

        # then change object to fit your requirements.
        # finally persist object in database

        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()

        return super(CreateView, self).form_valid(form)
