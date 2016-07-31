"""steelrumors URL <Configuration></Configuration>

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import links.views as links_views
from django.contrib.auth.decorators import login_required as auth


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('links.urls')),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r"^users/(?P<slug>\w+)/$", links_views.UserProfileDetailView.as_view(),
        name="profile"),
    url(r"^edit_profile/$", auth(links_views.UserProfileEditView.as_view()),
        name="edit_profile"),
    url(r"^link/create/$", auth(links_views.LinkCreateView.as_view()),
        name='link_create'),
    url(r'^link/(?P<pk>\d+)/$', links_views.LinkDetailView.as_view(),
        name='link_detail'),
    url(r'^link/update/(?P<pk>\d+)/$',
        auth(links_views.LinkUpdateView.as_view()), name='link_update'),
    url(r'^link/delete/(?P<pk>\d+)/$',
        auth(links_views.LinkDeleteView.as_view()), name='link_delete')
]
