#!flask/bin/python
# -*- coding: utf-8 -*-
import urllib2
from app import db, log_message
from app.decorators import async
from app.models import Novelty
from bs4 import BeautifulSoup
from config import UPDATE_FREQUENCY, SITES
import feedparser
import time
from datetime import datetime, timedelta


def parse_site(feed_url, site_name):
    d = feedparser.parse(feed_url)
    if site_name in ('postimees', 'naistekas'):
        for entry in d['entries']:
            url = entry['links'][0]['href']
            novelty = Novelty.query.filter_by(url=url).first()
            if novelty is None:
                headline = entry['title']
                published_date = datetime(*entry['published_parsed'][:6])
                comments_count = get_comments_count(url, site_name)
                last_update = datetime.utcnow() if comments_count else None
                novelty = Novelty(url=url,
                                  site=site_name,
                                  headline=headline,
                                  comments_count=comments_count,
                                  last_update=last_update,
                                  published_date=published_date)
                db.session.add(novelty)
                db.session.commit()
    else:
        for entry in d['entries']:
            url = entry['feedburner_origlink']
            novelty = Novelty.query.filter_by(url=url).first()
            if novelty is None:
                headline = entry['title']
                published_date = datetime(*entry['published_parsed'][:6])
                comments_count = get_comments_count(url, site_name)
                last_update = datetime.utcnow() if comments_count else None
                novelty = Novelty(url=url,
                                  site=site_name,
                                  headline=headline,
                                  comments_count=comments_count,
                                  last_update=last_update,
                                  published_date=published_date)
                db.session.add(novelty)
                db.session.commit()


def get_comments_count(novelty_url, site_name):
    if site_name == "postimees":
        try:
            response = urllib2.urlopen(novelty_url)
            soup = BeautifulSoup(response.read())
            article_title = soup.find_all(attrs={"class": "com"})[0]
            count = article_title.find_all("a")[0].contents[0]
            count = count.replace('(', '').replace(')', '')
            return int(count)
        except:
            return 0
    else:
        try:
            response = urllib2.urlopen(novelty_url)
            soup = BeautifulSoup(response.read())
            article_title = soup.find_all(attrs={"class": "articleTitle"})[0]
            count = article_title.find_all("a")[0].contents[0]
            count = count.replace('(', '').replace(')', '')
            return int(count)
        except:
            return 0


@async
def parse_sites(once=False):
    while True:
        for site_name, feed_url in SITES.items():
            try:
                parse_site(feed_url, site_name.decode('utf-8'))
            except:
                log_message("parse_sites() failed on %s" % datetime.utcnow())
            time.sleep(UPDATE_FREQUENCY)
        if once:
            break


@async
def update_comment_counts(days, interval_min, once=False):
    while True:
        for site in SITES:
            date_from = datetime.utcnow() - timedelta(days=days)
            novelties = Novelty.query.filter(Novelty.published_date > date_from).filter(Novelty.site == site)
            for novelty in novelties:
                count = get_comments_count(novelty.url, novelty.site)
                if count > novelty.comments_count:
                    novelty.comments_count = count
                    db.session.add(novelty)
                    db.session.commit()
                time.sleep(0.3)
        if once:
            break
        time.sleep(interval_min * 60)


@async
def delete_older_novelties():
    while True:
        date_from = datetime.utcnow() - timedelta(days=8)
        novelties = Novelty.query.filter(Novelty.published_date < date_from).filter(Novelty.comments_count < 30)
        for novelty in novelties:
            db.session.delete(novelty)
            db.session.commit()
        time.sleep(3600 * 24)


@async
def update_all_sites(once=False):
    delete_older_novelties()
    update_comment_counts(1, 30, once)
    time.sleep(5 * 60)
    update_comment_counts(3, 200, once)
    time.sleep(30 * 60)
    update_comment_counts(7, 500, once)


if __name__ == '__main__':
    delete_older_novelties()
    #parse_sites(True)
    #update_all_sites(True)