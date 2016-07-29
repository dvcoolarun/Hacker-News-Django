from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from .models import Link, Vote, UserProfile

from django.shortcuts import render
from django.views import generic


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
