#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from datetime import date

AUTHOR = u'Bob McKee'
SITENAME = u'Colt Daggerfist'
SITEURL = 'http://localhost:8000'

TIMEZONE = 'America/New_York'

COPYRIGHT = 'Copyright &copy; %s Robert McKee. All rights reserved.' % date.today().year
COPYRIGHT_NAME = 'Robert McKee'

DATE_FORMATS = {
    'en': '%B %d, %Y',
}

DEFAULT_LANG = u'en'

DEFAULT_PAGINATION = 3

DISQUS_SITENAME = 'dev-bywires'

ARTICLE_DIR = 'articles'
ARTICLE_URL = 'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{category}/{slug}/index.html'

CATEGORY_URL = 'articles/{slug}/'
CATEGORY_SAVE_AS = 'articles/{slug}/index.html'
CATEGORIES_SAVE_AS = False

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

TAG_SAVE_AS = False
TAGS_SAVE_AS = False

AUTHOR_SAVE_AS = False

ARCHIVES_SAVE_AS = False

PLUGINS = [
    'pelican.plugins.assets', 
    'pelican.plugins.sitemap',
    ]

WEBASSETS = True

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

THEME = 'themes/bywires'

FEED_ALL_RSS = 'feeds/all.rss'

FILES_TO_COPY = (
    ('extra/.htaccess', '.htaccess'), 
    ('extra/robots.txt', 'robots.txt'),
    ('extra/favicon.gif', 'favicon.gif'),
    ('extra/favicon.ico', 'favicon.ico'),
    )
