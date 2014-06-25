# -*- coding: utf-8 -*-
from collections import OrderedDict
import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'This is a secret!'


if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# pagination
POSTS_PER_PAGE = 20

# Update
UPDATE_FREQUENCY = 120

# Sites
SITES = OrderedDict([('delfi', 'http://feeds2.feedburner.com/delfiuudised'),
         ('postimees', 'http://www.postimees.ee/rss/'),
         ('epl', 'http://feeds.feedburner.com/eestipaevaleht'),
         ('ekspress', 'http://feeds.feedburner.com/EestiEkspressFeed'),
         ('sport', 'http://feeds2.feedburner.com/delfisport'),
         ('arileht', 'http://feeds2.feedburner.com/delfimajandus'),
         ('forte', 'http://feeds2.feedburner.com/forteuudised'),
         ('maaleht', 'http://feeds2.feedburner.com/maaleht'),
         ('publik', 'http://feeds2.feedburner.com/publikuudised'),
         ('naistekas', 'http://feeds2.feedburner.com/naistekas'),
         ])