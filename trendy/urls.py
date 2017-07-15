"""
Urls for the trendy Opal plugin
"""
from django.conf.urls import patterns, url

from trendy import views

urlpatterns = patterns(
    '',
    url('^trendy/$', views.TrendyView.as_view(), name="trends"),
)
