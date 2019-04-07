from app.models import Poll, blogs
from urllib.request import urlopen, Request as req
from bs4 import BeautifulSoup, CData
from datetime import datetime
from app import db, cleaning, book_creator

def main():
	print("entered main")
	startPoll()

def startPoll():
	print("polling")

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	for blog in blogs:
		# Thread(target=createEbook, name=blog, args=(current_app._get_current_object(), blog, headers)).start()
		createEbook(blog, headers)

	threading.Timer(3600, poll).start()
	# r = Response(str("polling"), status=200)
	# return r

def createEbook(blog, headers):
		url = blogs[blog]['url']
		print("inside ebook")

		toSend = req(url=url, headers=headers)

		xml = urlopen(toSend).read()
		rss_feed = BeautifulSoup(xml, 'xml')

		# Find last build date. If none, set to default date 11 Mar 2019
		new_update = rss_feed.find('lastBuildDate')
		if new_update is not None:
			new_update = datetime.strptime(rss_feed.find('lastBuildDate').text.strip(), "%a, %d %b %Y %H:%M:%S +0000")
		else:
			print("rss feed for {} has no default time".format(blog))
			new_update = DEFAULT_TIME

		# Retrieve last date polled from database
		# if not in database, create new poll entry
		last_updated = Poll.query.filter(Poll.name == blog).first()

		if last_updated.time == new_update:
			print("skipping {}".format(blog))
			return

		if last_updated is None:
			new_time = datetime.strptime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
			last_updated = Poll(name=blog, time=new_time)
			db.session.add(last_updated)
		else:
			print("setting new time for {}. Time is: {}".format(blog, new_update))
			last_updated.time = new_update

		db.session.commit()

		print("creating {}".format(blog))

		parseWorker(blog)

		book_creator.createEBook(blog)

if __name__== "__main__":
	main()