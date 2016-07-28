from django.shortcuts import render
from django.views import generic

from .models import Link, Vote


class LinkListView(generic.ListView):
    model = Link
