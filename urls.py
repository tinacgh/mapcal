from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from mapcal import views

# ADD to mysite/urls.py:
# url(r'^mapcal/', include('mapcal.urls')),
#  ('mapcal.urls' is inside quotes)

urlpatterns = patterns('',
    url(r'^$', views.listappts),
    url(r'^all/$', views.listallappts),
    url(r'^bytag/$', views.bytag),
    url(r'^(?P<appt_id>\d+)/detail/$', views.detail, name="appt_detail"),
    url(r'^add/$', views.add),
    url(r'^delete/$', views.delete_appt),
    url(r'^accounts/login/$', login),
    url(r'^accounts/dologin/$', views.mapcal_login),
    url(r'^accounts/logout/$', views.logout_view),
)
                       
