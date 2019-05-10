import threading
from urllib.request import urlopen, Request as req
from flask import render_template, request, Response, redirect, flash, url_for, current_app
from flask_login import current_user, login_required
import time
from datetime import datetime
from time import gmtime
from threading import Thread
from bs4 import BeautifulSoup, CData
import pickle
import json
from app import db, cleaning, book_creator, email
from app.models import User, Blog, BlogName, Poll, blogs
from app.main import bp
from werkzeug.urls import url_parse
import os

DEFAULT_TIME = datetime.strptime("Mon, 11 Mar 2019 17:45:34 +0000", "%a, %d %b %Y %H:%M:%S +0000")

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)

#@login_required
@bp.route('/poll', methods=['GET'])
def poll():
	print("polling")

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

	for blog in blogs:
		# Thread(target=createEbook, name=blog, args=(current_app._get_current_object(), blog, headers)).start()
		createEbook(current_app._get_current_object(), blog, headers)

	threading.Timer(3600, poll).start()
	r = Response(str("polling"), status=200)
	return r

def createEbook(app, blog, headers):
	with app.app_context():
		url = blogs[blog]['url']

		toSend = req(url=url, headers=headers)

		xml = urlopen(toSend).read()
		rss_feed = BeautifulSoup(xml, 'xml')

		# Find last build date. If none, set to default date 11 Mar 2019
		new_update = rss_feed.find('lastBuildDate')
		if new_update is not None:
			new_update = datetime.strptime(rss_feed.find('lastBuildDate').text.strip(), "%a, %d %b %Y %H:%M:%S +0000")
		else:
			print("rss feed for {} has no default time".format(blog))
			new_update = datetime.now()

		# Retrieve last date polled from database
		# if not in database, create new poll entry
		last_updated = Poll.query.filter(Poll.name == blog).first()

		if last_updated.time == new_update:
			print("skipping {}".format(blog))
			return

		if last_updated is None:
			new_time = datetime.now()
			last_updated = Poll(name=blog, time=new_time)
			db.session.add(last_updated)
		else:
			print("setting new time for {}. Time is: {}".format(blog, new_update))
			last_updated.time = new_update

		db.session.commit()

		print("creating {}".format(blog))

		parseWorker(blog)

		book_creator.createEBook(blog)

		sendByBlog(blog)

def sendByBlog(name):
	users = Blog.query.filter(name == Blog.name).all()
	for user in users:
		desired = User.query.filter(user.id == User.id).first()
		kindle = desired.kindle_email
		email.send_kindle(sender=current_app.config['ADMINS'][0], recipients=[kindle_email], filename='../publishing/books/{}.mobi'.format(name))


@login_required
@bp.route('/parseRSS', methods=['POST'])
def parseRSS(name=None):
	if name is None:
		name = request.values.get('name')

	output = parseWorker(name)

	r = Response(str(output), status=200)
	return r

def parseWorker(name):
	print("name is {}".format(name))
	url = blogs[name]['url']

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	rss_feed = BeautifulSoup(xml, 'html.parser')

	output = rss_feed.find('item')

	if 'custom_parse' in blogs[name]:
		output =  cleaning.findFirst(name, output)
	else:
		max = 0

		for cd in output.findAll(text=True):
			if isinstance(cd, CData):
				if len(cd) > max:
					output = BeautifulSoup(cd, 'html.parser')
					max = len(cd)

	book_creator.createHTML(name, output)

	return output


@login_required
@bp.route('/reset', methods=['POST'])
def reset():
	if (current_user.id != 1):
		return
	for blog in BlogName:
		last_updated = Poll.query.filter(Poll.name == blog).first()
		if last_updated is None:
			poll = Poll(name=blog, time=DEFAULT_TIME)
			db.session.add(poll)
		else:
			last_updated.time = DEFAULT_TIME
		db.session.commit()

	r = Response(str("times reset"), status=200)
	return r

@bp.route('/')
@bp.route('/index')
@login_required
def index(name=None):
	return render_template('index.html', name=name)

@login_required
@bp.route('/blogs', methods=['GET'])
def get_blogs():
	choices = Blog.query.all()
	for choice in choices:
		if (choice.user_id == current_user.id):
			blogs[choice.name.name]['selected'] = True
	r = Response(json.dumps(blogs), status=200)
	return r

@login_required
@bp.route('/set_email', methods=['POST'])
def set_email():
	email = request.values.get('email')
	user = User.query.filter(User.id == current_user.id).first()
	user.kindle_email = email
	db.session.commit()

	r = Response("Email is {}".format(email), status=200)
	return r

@login_required
@bp.route('/kindle', methods=['GET'])
def kindle():
	user = User.query.filter(User.id == current_user.id).first()
	kindle = user.kindle_email
	r = Response(json.dumps(kindle), status=200)
	return r

@bp.route('/send', methods=['POST'])
def send():
	if (current_user.id != 1):
		return
	users = User.query.all()
	dicts = []

	for user in users:
		dicts.append(user.get_dict())

	print(dicts)

	for user in dicts:
		if (user['kindle_email'] is not None):
			print(os.getcwd())
			blogs = Blog.query.filter(Blog.user_id == current_user.id).all()
			for blog in blogs:
				email.send_kindle(sender=current_app.config['ADMINS'][0], recipients=[user['kindle_email']], filename='../publishing/books/{}.mobi'.format(blog.name.name))

	r = Response(("sent email"), status=200)
	return r

@login_required
@bp.route('/subscribe', methods=['POST'])
def subscribe():
	name = request.values.get('name')
	blog = Blog(user_id=current_user.id, name=name)
	check = Blog.query.filter(Blog.user_id == current_user.id).filter(Blog.name == name)
	if not check.all():
		db.session.add(blog)
		db.session.commit()
	r = Response("subscribed from {}".format(name), status=200)
	return r

@login_required
@bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
	name = request.values.get('name')
	queries = Blog.query.filter(Blog.user_id == current_user.id).filter(Blog.name == name).all()
	for query in queries:
		blogs[query.name.name]['selected'] = False
		db.session.delete(query)
	db.session.commit()
	r = Response("unsubscribed from {}".format(name), status=200)
	return r
