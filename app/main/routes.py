from urllib.request import urlopen, Request as req
from flask import render_template, request, Response, redirect, flash, url_for
from flask_login import current_user, login_required
import time, threading
from bs4 import BeautifulSoup, CData
import pickle
import json
from app import db, cleaning, book_creator
from app.models import User, Blog, BlogName, blogs
from app.main import bp
from werkzeug.urls import url_parse

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)

@login_required
@bp.route('/poll', methods=['POST'])
def poll():
	print("polling")

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

	for blog in blogs:
		url = blogs[blog]['url']

		toSend = req(url=url, headers=headers)

		xml = urlopen(toSend).read()
		rss_feed = BeautifulSoup(xml, 'xml')

		new_update = rss_feed.find('lastBuildDate')
		if new_update is not None:
			new_update = time.strptime(rss_feed.find('lastBuildDate').text.strip(), "%a, %d %b %Y %H:%M:%S +0000")
		else:
			new_update = time.strptime("Mon, 11 Mar 2019 17:45:34 +0000", "%a, %d %b %Y %H:%M:%S +0000")

		file = open('last.txt', 'rb')
		time_table = pickle.load(file)
		file.close()

		last_updated = time.strptime("Mon, 11 Mar 2019 17:45:34 +0000", "%a, %d %b %Y %H:%M:%S +0000")
		if blog in time_table:
			last_updated = time.strptime(time_table[blog].strip(), "%a, %d %b %Y %H:%M:%S +0000")

		# if no new update do nothing
		if last_updated == new_update:
			print("skipping {}".format(blog))
			continue

		time_table[blog] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", new_update)
		file = open('last.txt', 'wb')
		pickle.dump(time_table, file)
		file.close()

		print("creating {}".format(blog))

		parseRSS(blog)

		book_creator.createEBook(blog)

	threading.Timer(3600, poll).start()
	r = Response(str("polling"), status=200)
	return r

@login_required
@bp.route('/parseRSS', methods=['POST'])
def parseRSS(name=None):
	if name is None:
		name = request.values.get('name')

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


	open( './publishing/html/' + name + '.html', 'w').close()
	text_file = open('./publishing/html/' + name + ".html", "w")
	text_file.write(str(output))
	text_file.close()

	r = Response(str(output), status=200)
	return r

@login_required
@bp.route('/reset', methods=['POST'])
def reset():
	file = open('last.txt', 'rb')
	time_table = pickle.load(file)
	file.close()

	for key in time_table:
		time_table[key] = "Mon, 11 Mar 2019 17:45:34 +0000"

	file = open('last.txt', 'wb')
	pickle.dump(time_table, file)
	file.close()
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
