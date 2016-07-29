from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', views.LinkListView.as_view(), name='home'),
]
