# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, g
from app import app, db
from forms import CommentForm
from markupsafe import Markup
from models import Novelty, Comment
from datetime import datetime, timedelta
from config import POSTS_PER_PAGE, SITES
from werkzeug.exceptions import abort


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


sites = {'all': "Kõik"}
for site in SITES:
    sites[site] = site.capitalize()

if 'arileht' in sites:
    sites['arileht'] = "Ärileht"

time_modes = {'today': {'days': timedelta(days=1), 'title': "Viimased 24h | Enim kommenteeritud", 'time_button_text': "24h"},
              'last-three-days': {'days': timedelta(days=3), 'title': "Viimased 3 päeva | Enim kommenteeritud", 'time_button_text': "3 päeva"},
              'last-week': {'days': timedelta(days=7), 'title': "Viimane nädal | Enim kommenteeritud", 'time_button_text': "nädal"},
              'last-month': {'days': timedelta(days=30), 'title': "Viimane kuu | Enim kommenteeritud", 'time_button_text': "kuu"},
              'last-year': {'days': timedelta(days=365), 'title': "Viimane aasta | Enim kommenteeritud", 'time_button_text': "aasta"},
}


def nav_bar_times():
    time_mode_keys = ('today', 'last-three-days', 'last-week', 'last-month', 'last-year')
    html = ''
    for time_mode in time_mode_keys:
        active = ''
        if g.time_mode == time_mode:
            active = ' class=\"active\"'
        url = url_for('render_novelties', time_mode=time_mode, site=g.site)
        text = time_modes[time_mode]['time_button_text']
        html += "<li%s><a href=\"%s\">%s</a></li>" % (active, url, text)
    return Markup(html.decode('utf-8'))


def nav_bar_sites():
    site_names = ['all']
    site_names.extend(SITES)
    html = ''
    for site in site_names:
        active = ''
        if g.site == site:
            active = ' class=\"active\"'
        url = url_for('render_novelties', time_mode=g.time_mode, site=site)
        html += "<li%s><a href=\"%s\">%s</a></li>" % (active, url, sites[site])

    return Markup(html.decode('utf-8'))


@app.route('/')
@app.route('/<site>/')
@app.route('/<site>/<time_mode>')
@app.route('/<site>/<time_mode>/<int:page>')
def render_novelties(site='all', time_mode='today', page=1):
    if site not in sites and not time_mode:
        abort(404)
    if site and time_mode and (time_mode not in time_modes or site not in sites):
        abort(404)

    g.time_mode = time_mode
    g.site = site
    date_from = datetime.utcnow() - time_modes[time_mode]['days']
    if g.site != 'all':
        novelties = Novelty.query.filter(Novelty.published_date > date_from).filter(Novelty.site == g.site).order_by(
            Novelty.comments_count.desc()).paginate(page, POSTS_PER_PAGE, False)
    else:
        novelties = Novelty.query.filter(Novelty.published_date > date_from).order_by(
            Novelty.comments_count.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                           title=time_modes[time_mode]['title'].decode('utf-8'),
                           novelties=novelties)


@app.route('/novelty/<int:novelty_id>', methods=['GET', 'POST'])
def novelty_discussion(novelty_id):
    novelty = Novelty.query.filter(Novelty.id == novelty_id).first()
    if not novelty:
        abort(404)
    if novelty.comments().count() == 0:
        flash("Ole esimene, kes artiklit kommenteerib!")
    form = CommentForm()
    if form.validate_on_submit() and not form.nickname.data:
        comment = Comment(body=form.comment.data,
                          timestamp=datetime.utcnow(),
                          nickname=form.nimi.data,
                          novelty_id=novelty_id)
        db.session.add(comment)
        db.session.commit()
        flash('Kommentaar lisatud!')
        return redirect(url_for('novelty_discussion', novelty_id=novelty_id))
    return render_template('novelty_discussion.html', title=novelty.headline,
                           novelty=novelty, form=form)