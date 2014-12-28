# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponsePermanentRedirect, HttpResponseNotFound)

from suorx import settings
from shortner import UrlShortner

from urlshorten.models import ShortenUrls

import urlparse
import pylibmc
import json
import os


def home(request):
    '''
    Main website
    '''
    return render(request, 'index.html')


def shorten(request):
    '''
    Shorten a users URL and if they URL has already been shortened
    retrieve the short URL from cache
    '''
    url = request.POST.get('url', None)

    shorten = UrlShortner()

    # Grab Memcached Details
    servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
    username = os.environ.get('MEMCACHIER_USERNAME', '')
    password = os.environ.get('MEMCACHIER_PASSWORD', '')

    has_cache = True
    has_database = True

    if url is None:
        return HttpResponseNotFound('404')
    else:
        mc = pylibmc.Client(
            servers,
            username=username,
            password=password,
            binary=True,
            behaviors={'tcp_nodelay': True, 'ketama': True, 'no_block': True}
        )

    if 'http' in urlparse.urlparse(url).scheme:
        pass
    elif urlparse.urlparse(url).scheme == '':
        url = 'http://' + url
    else:
        return HttpResponseBadRequest('Invalid URL')

    site_code = shorten.encode(url)
    _cache_url = mc.get(site_code)

    # Cache the users shortened URL and log URL
    if _cache_url:
        return HttpResponse(
            json.dumps({'url': '/'.join([settings.DOMAIN, site_code])}),
            content_type="application/json"
        )

    if not mc.set(site_code, url):
        has_cache = False

    try:
        site = ShortenUrls.objects.get(short__exact=url)
    except ShortenUrls.DoesNotExist:
        site = ShortenUrls(url=url, short=site_code, no_clicks=0)
        site.save()

    return HttpResponse(
        json.dumps({'url': '/'.join([settings.DOMAIN, site.short])}),
        content_type="application/json"
    )


def redirect(request, url):
    '''
    Redirect all shorten URL's to their original url
    '''
    # Grab Memcached Details
    servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
    username = os.environ.get('MEMCACHIER_USERNAME', '')
    password = os.environ.get('MEMCACHIER_PASSWORD', '')

    mc = pylibmc.Client(
        servers,
        username=username,
        password=password,
        binary=True,
        behaviors={'tcp_nodelay': True, 'ketama': True, 'no_block': True}
    )

    origin = mc.get(url)

    if origin:
        return HttpResponsePermanentRedirect(origin)
    else:
        try:
            site = ShortenUrls.objects.get(short__exact=url)

            return HttpResponsePermanentRedirect(site.url)
        except ShortenUrls.DoesNotExist:
            return HttpResponseNotFound('')
