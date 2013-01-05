#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
sys.path.append('.')
from pelicanconf import *

SITEURL = 'http://blog.bywires.com'

DISQUS_SITENAME = 'bywires'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# Uncomment following line for absolute URLs in production:
RELATIVE_URLS = False

GOOGLE_ANALYTICS = ''

BITLY_USERNAME = ''
BITLY_API_KEY = ''

PLUGINS.append('pelican-bitly')
