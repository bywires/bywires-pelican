#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Bob McKee'
SITENAME = u'Bywires.com'
SITEURL = ''

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

DEFAULT_PAGINATION = 5

ARTICLE_URL = 'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{category}/{slug}/index.html'

PLUGINS = ['pelican.plugins.assets']

THEME = 'themes/bywires'

WEBASSETS = True
