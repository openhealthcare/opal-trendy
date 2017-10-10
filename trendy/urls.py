"""
Urls for the trendy Opal plugin
"""
from __future__ import unicode_literals


from django.conf.urls import patterns, url

from trendy import views

urlpatterns = patterns(
    '',
    url('^trendy$', views.TrendyList.as_view(), name="trendy_home"),
    url('^trendy/(?P<list>[0-9a-z_\-]+/?)/episodes$', views.TrendyEpisodeView.as_view(), name="trendy_episodes"),
    url('^trendy/(?P<list>[0-9a-z_\-]+/?)$', views.TrendyPatientList.as_view(), name="trendy_patient_list"),
    # url('^trendy/$', views.TrendyView.as_view(), name="trends"),
    # url('^/trend_subrecord_loader/$', views.TrendyLoader.as_view(), name="trends"),
)
