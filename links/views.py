import django.views.generic as generic_views
import django.views.generic.edit as generic_edit
from django.contrib.auth import get_user_model
import links.models as links_models

from django.shortcuts import render
from django.views import generic

import links.forms as links_forms

from django.core.urlresolvers import reverse, reverse_lazy
from django_comments.models import Comment

# import for the vote form
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from .forms import VoteForm
from .models import Vote
from .models import Link
import json
from django.http import HttpResponse

# a mixin is a class that contains methods for use by other classes
# without being inherited by other classes.

# get_context_data(**kwargs)
# Returns a dictionary respresenting a template context.
# The keyword arguments provided will make up the returned context


class RandomGossipMixin(object):

    def get_context_data(self, **kwargs):
        context = super(RandomGossipMixin, self).get_context_data(**kwargs)
        context["randomquip"] = Comment.objects.order_by('?')[0]
        return context


class LinkListView(RandomGossipMixin, generic_views.ListView):
    model = links_models.Link
    queryset = links_models.Link.with_votes.all()
    paginate_by = 3


class UserProfileDetailView(generic_views.DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        links_models.UserProfile.objects.get_or_create(user=user)
        return user


# For Editing your Profile Details
class UserProfileEditView(generic_edit.UpdateView):
    model = links_models.UserProfile
    form_class = links_forms.UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return links_models.UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})


class LinkCreateView(generic_edit.CreateView):
    model = links_models.Link
    form_class = links_forms.LinkForm

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

        return super(generic_edit.CreateView, self).form_valid(form)


class LinkDetailView(generic_views.DetailView):
    model = links_models.Link


class LinkUpdateView(generic_edit.UpdateView):
    model = links_models.Link
    form_class = links_forms.LinkForm


class LinkDeleteView(generic_edit.DeleteView):
    model = links_models.Link
    links_forms.success_url = reverse_lazy("home")


# Mixin to Implement a JSON response for our
# AJAX requests.

class JSONFormMixin(object):

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(
            vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response


class VoteFormBaseView(FormView):
    form_class = VoteForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        link = get_object_or_404(Link, pk=form.data["link"])
        user = self.request.user
        prev_votes = Vote.objects.filter(voter=user, link=link)
        has_voted = (len(prev_votes) > 0)

        ret = {"success": 1}
        if not has_voted:
            # add vote
            v = Vote.objects.create(voter=user, link=link)
            ret["voteobj"] = v.id
        else:
            # delete vote
            prev_votes[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)

    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form_errors}
        return self.create_response(ret, False)


class VoteFormView(JSONFormMixin, VoteFormBaseView):
    pass
