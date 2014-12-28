from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'urlshorten.views.home', name='home'),
    url(r'^shorten/$', 'urlshorten.views.shorten', name='shorten'),
    url(r'^([A-Za-z0-9]{1,25})/$', 'urlshorten.views.redirect', name='redirect'),
)
