from app import app
from urllib.request import urlopen
from urllib.request import Request as req
from flask import render_template, request, Response
import time, threading
from bs4 import BeautifulSoup, CData
import pickle
from flask_mail import Mail, Message
import os
import json
from app import cleaning
from app import book_creator
from flask_mail import Mail, Message
from flask_login import current_user, login_user
from app.models import User

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)

data = {
	'stratechery': {
		'display': "Stratechery",
		'url': "https://stratechery.com/feed",
	},
	'startupboy':
	{
		'display': "Startupboy",
		'url': "https://startupboy.com/feed",
	},
	'bryan_caplan_econlib':
	{
		'display': 'Bryan Caplan\'s Econlib',
		'url': "https://www.econlib.org/feed/indexCaplan_xml",
	},
	'marginal_revolution':
	{		
		'display': "Marginal Revolution",
		'url': "https://feeds.feedburner.com/marginalrevolution/",
	},
	'ribbonfarm':
	{
		'display': "Ribbon Farm",
		'url': "https://ribbonfarm.com/feed",
		'custom_parse': True
	},
	'melting_asphalt':
	{
		'display': "Melting Asphalt",
		'url': "https://feeds.feedburner.com/MeltingAsphalt",
	},
	'overcoming_bias':
	{
		'display': 'Overcoming Bias',
		'url': "http://www.overcomingbias.com/feed",
	},
	'elaine_ou':
	{
		'display': 'Elaine Ou',
		'url': 'https://elaineou.com/feed/',
	},
	'eugene_wei':
	{
		'display': 'Eugene Wei',
		'url': 'https://eugene-wei.squarespace.com/blog?format=rss'
	},
	'meaningness':
	{
		'display': 'Meaningness',
		'url': 'https://meaningness.com/rss.xml',
		'custom_parse': True
	}

}

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
def index(name=None):
	user = {'username': 'Rahul'}
	return render_template('index.html', name=name, user=user)

@app.route('/blogs', methods=['GET'])
def blogs():
	r = Response(json.dumps(data), status=200)
	return r

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
	print("times resetted")
	r = Response(str("times reset"), status=200)
	return r

@app.route('/parseRSS', methods=['POST'])
def parseRSS(name=None):
	if name is None:
		name = request.values.get('name')

	url = data[name]['url']

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	rss_feed = BeautifulSoup(xml, 'html.parser')

	output = rss_feed.find('item')

	if 'custom_parse' in data[name]:
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

@app.route('/poll', methods=['POST'])
def poll():
	print("polling")

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

	for blog in data:
		url = data[blog]['url']

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

@app.route('/send')
def send():
	print("sending email")
	recipient = request.values.get('recipient')
	print(recipient)
	msg = Message(
		subject="Hello",
		sender=app.config.get("MAIL_USERNAME"),
		recipients=["rahul@sarathy.org"],
		body="This is a test email I sent with Gmail and Python")
	mail.send(msg)
	r = Response(str("mailing"), status=200)
	return r