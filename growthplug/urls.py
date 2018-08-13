from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from user import views as core_views
from user.views import post_data,display_users,update_data,delete_data

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^login_user$', core_views.login_user, name='login_user'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^post/', post_data),
    url(r'^display_users/', display_users),
    url(r'^update_data/(\d+)$', update_data),
    url(r'^delete_data/(\d+)$', delete_data),
]
