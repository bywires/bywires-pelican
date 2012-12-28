#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Bob McKee'
SITENAME = u'Bywires.com'
SITEURL = ''

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

ARTICLE_URL = 'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{category}/{slug}/index.html'

THEME = 'themes/bywires'
