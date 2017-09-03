"""
Urls for the trendy Opal plugin
"""
from django.conf.urls import patterns, url

from trendy import views

urlpatterns = patterns(
    '',
    url('^trendy/list$', views.TrendyList.as_view(), name="trendy_home"),
    # url('^trendy/$', views.TrendyView.as_view(), name="trends"),
    # url('^/trend_subrecord_loader/$', views.TrendyLoader.as_view(), name="trends"),
)
