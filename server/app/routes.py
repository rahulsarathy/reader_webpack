from urllib.request import urlopen, Request as req
from flask import render_template, request, Response, redirect, flash, url_for
import time, threading
from bs4 import BeautifulSoup, CData
import pickle
import os
import json
from app import app, db, cleaning, book_creator
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Blog, BlogName
from app.forms import LoginForm, ResetPasswordRequestForm, RegistrationForm, ResetPasswordForm
from app.email import send_password_reset_email
from werkzeug.urls import url_parse

blogs = {
	'stratechery': {
		'display': "Stratechery",
		'url': "https://stratechery.com/feed",
		'category': ['technology']
	},
	'startupboy':
	{
		'display': "Startupboy",
		'url': "https://startupboy.com/feed",
		'category': ['technology']

	},
	'bryan_caplan_econlib':
	{
		'display': 'Bryan Caplan\'s Econlib',
		'url': "https://www.econlib.org/feed/indexCaplan_xml",
		'category': ['economics']

	},
	'marginal_revolution':
	{		
		'display': "Marginal Revolution",
		'url': "https://feeds.feedburner.com/marginalrevolution/",
		'category': ['economics']
	},
	'ribbonfarm':
	{
		'display': "Ribbon Farm",
		'url': "https://ribbonfarm.com/feed",
		'custom_parse': True,
		'category': ['rationality']
	},
	'melting_asphalt':
	{
		'display': "Melting Asphalt",
		'url': "https://feeds.feedburner.com/MeltingAsphalt",
		'category': ['rationality']
	},
	'overcoming_bias':
	{
		'display': 'Overcoming Bias',
		'url': "http://www.overcomingbias.com/feed",
		'category': ['rationality', 'economics']
	},
	'elaine_ou':
	{
		'display': 'Elaine Ou',
		'url': 'https://elaineou.com/feed/',
		'category': ['personal_musings']
	},
	'eugene_wei':
	{
		'display': 'Eugene Wei',
		'url': 'https://eugene-wei.squarespace.com/blog?format=rss',
		'category': ['personal_musings'],
	},
	'meaningness':
	{
		'display': 'Meaningness',
		'url': 'https://meaningness.com/rss.xml',
		'category': ['rationality'],
		'custom_parse': True,
	},
	'cato': {
		'display': 'Cato Institute',
		'url': 'https://www.cato.org/rss/recent-opeds',
		'category': ['think_tanks'],
		'custom_parse': True
	},
	'aei': {
		'display': 'American Enterprise Institute',
		'url': 'https://http://www.aei.org/feed/',
		'category': ['think_tanks'],
		'custom_parse': True
	},
	'brookings': {
		'display': 'Brookings Institution',
		'url': 'http://feeds.feedblitz.com/BrookingsRSS/programs/economics',
		'category': ['think_tanks', 'economics'],
		'custom_parse': True
	},
	'niskanen': {
			'display': 'Niskanen Center',
			'url': 'https://niskanencenter.org/feed/',
			'category': ['think_tanks', 'economics'],
	},
	'mercatus': {
		'display': 'Mercatus Center',
		'url': 'https://www.mercatus.org/feed',
		'category': ['think_tanks', 'economics'],
		'custom_parse': True
	}, 
	'pew': {
		'display': 'Pew Research Center',
		'url': 'http://www.pewresearch.org/feed/',
		'category': ['think_tanks']
	}
}

@app.route('/')
@app.route('/index')
@login_required
def index(name=None):
	return render_template('index.html', name=name)

@login_required
@app.route('/blogs', methods=['GET'])
def get_blogs():
	choices = Blog.query.all()
	for choice in choices:
		if (choice.user_id == current_user.id):
			blogs[choice.name.name]['selected'] = True
	r = Response(json.dumps(blogs), status=200)
	return r

@login_required
@app.route('/subscribe', methods=['POST'])
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
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
	name = request.values.get('name')
	queries = Blog.query.filter(Blog.user_id == current_user.id).filter(Blog.name == name).all()
	for query in queries:
		blogs[query.name.name]['selected'] = False
		db.session.delete(query)
	db.session.commit()
	r = Response("unsubscribed from {}".format(name), status=200)
	return r

@login_required
@app.route('/reset', methods=['POST'])
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

@login_required
@app.route('/parseRSS', methods=['POST'])
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
@app.route('/poll', methods=['POST'])
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)