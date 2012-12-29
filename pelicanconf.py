#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Bob McKee'
SITENAME = u'Bywires.com'
SITEURL = ''

TIMEZONE = 'America/New_York'

DATE_FORMATS = {
    'en': '%B %d, %Y',
}

DEFAULT_LANG = u'en'

DEFAULT_PAGINATION = 3

ARTICLE_URL = 'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{category}/{slug}/index.html'
ARTICLE_EXCLUDES = ('pages',)

CATEGORY_URL = 'articles/{slug}/'
CATEGORY_SAVE_AS = 'articles/{slug}/index.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

PLUGINS = ['pelican.plugins.assets']

WEBASSETS = True

THEME = 'themes/bywires'

FEED_ALL_RSS = 'feeds/all.rss'
