from django.conf.urls import patterns, include, url

from mapcal import views

# ADD to mysite/urls.py:
# url(r'^mapcal/', include('mapcal.urls')),
#  ('mapcal.urls' is inside quotes)

urlpatterns = patterns('',
    url(r'^bytag/$', views.bytag),
    url(r'^(?P<appt_id>\d+)/detail/$', views.detail, name="appt_detail"),
    url(r'^add/$', views.add),
)
                       