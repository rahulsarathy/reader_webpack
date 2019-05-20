from config import Config
import sqlite3
import datetime
from app.models import blogs
from app import book_creator, email
from urllib.request import urlopen, Request as req
from bs4 import BeautifulSoup, CData

configuration = Config()

def startPoll():

	conn = sqlite3.connect('app.db')

	c = conn.cursor()

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

	#for each blog, check when it was last polled. If not polled in the last hour, then repoll

	# if there is a new post (store post dates in database) then create ebook for that post and send
	for blog in blogs:
		 c.execute(''' INSERT OR IGNORE INTO POLL
		 	(name, last_time, last_post) 
		 	VALUES
		 	(?, ?, ?)''', 
		 	(blog, '', ''))
		 conn.commit()

	c.execute('SELECT * FROM poll')
	rows = c.fetchall()
	for row in rows:
		
		name = row[0]
		last_time = row[1]
		last_post = row[2]

		# if last updated time exists, find latest poll and see if it is new enough for updating (1 hour)
		if last_time is not "":
			last_updated = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S.%f')
			diff = datetime.datetime.now() - last_updated
			# if blog was last polled over an hour ago
			if (diff.total_seconds() > 1):
				print("entered second")

				url = blogs[name]['url']
				toSend = req(url=url, headers=headers)
				xml = urlopen(toSend).read()
				rss_feed = BeautifulSoup(xml, 'xml')

				#find latest post date
				new_update = rss_feed.find('lastBuildDate')
				if new_update is not None:
					new_update = datetime.datetime.strptime(rss_feed.find('lastBuildDate').text.strip(), "%a, %d %b %Y %H:%M:%S +0000")
				else:
					print("rss feed for {} has no default time".format(blog))
					new_update = rss_feed.find('guid')

				#if there is a new post, update with new post
				if new_update != last_post:
					update_poll(conn, (name, datetime.datetime.now(), new_update))
					# create new post
					parseWorker(name)
					book_creator.createEBook(name)

					sendByBlog(conn, name)
					return

		#update_poll(conn, (name, datetime.datetime.now(), last_post))
		print("executing")
		c.execute('''UPDATE poll SET last_time = ? , last_post = ? 
			WHERE name = ?''', (datetime.datetime.now(), last_post, name))
		conn.commit()


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


def update_poll(conn, poll):
    """
    update poll, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE poll
              SET last_time = ? ,
                  last_post = ?
              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, poll)

# def sendByBlog(conn, name):
# 	''' '''
# 	cur = conn.cursor()
# 	cur.execute(''' SELECT * from blog WHERE name=?''', (name,))
# 	rows = cur.fetchall()
# 	print(rows)
# 	users = Blog.query.filter(name == Blog.name).all()
# 	print("users are {}".format(users))
# 	for user in users:
# 		desired = User.query.filter(user.user_id == User.id).first()
# 		print("desired is {}".format(desired))
# 		if desired is None:
# 			return
# 		kindle = desired.kindle_email
# 		if kindle is None:
# 			return
# 		email.send_kindle(sender=current_app.config['ADMINS'][0], recipients=[kindle], filename='../publishing/books/{}.mobi'.format(name))


def sendByBlog(conn, name):

	cur = conn.cursor()
	cur.execute(''' SELECT * from blog WHERE name=?''', (name,))
	rows = cur.fetchall()
	for row in rows:
		row_id = row[0]
		user_id = row[1]
		row_name = row[2]

		cur.execute(''' SELECT kindle_email from user WHERE id=?''', (user_id,))
		users = cur.fetchall()
		for user in users:
			kindle = user[0]
			if kindle is None:
				return
			email.send_kindle(sender=configuration.ADMINS[0], recipients=[kindle], filename='../publishing/books/{}.mobi'.format(name))


startPoll()


