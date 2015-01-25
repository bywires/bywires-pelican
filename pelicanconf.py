#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from datetime import date

AUTHOR = u'Bob McKee'
SITENAME = u'Daggerfist'
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

FB_ADMINS = 'bywires'

ARTICLE_PATHS = ['articles']
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

LOAD_CONTENT_CACHE = False

PLUGIN_PATHS = ['plugins']

PLUGINS = [
    'assets',
    'sitemap',
]

WEBASSETS = True

JINJA_EXTENSIONS = [
    'jinja2.ext.do',
]

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

EXTRA_PATH_METADATA = {
    'extra/.htaccess': {'path': '.htaccess'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

STATIC_PATHS = [
    'extra/.htaccess',
    'extra/robots.txt',
    'extra/favicon.ico'
]

MD_EXTENSIONS = ['fenced_code', 'codehilite(css_class=codehilite, linenums=True)', 'extra']