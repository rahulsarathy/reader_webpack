from newspaper import Article
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request as req
import pickle
import time

def findFirst(url, name):
	# url = 'https://stratechery.com/feed'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	rss_feed = BeautifulSoup(xml, 'xml')

	links = rss_feed.find_all('guid')
	if not links:
		links = rss_feed.find_all('link') 

	firstArticle = returnFirst(links)

	#clean html
	soup = specificArticle(name, firstArticle)
	soup = cleanTags(soup)
	soup = cleanAttributes(soup)

	open( './publishing/html/' + name + '.html', 'w').close()
	text_file = open('./publishing/html/' + name + ".html", "w")
	text_file.write(str(soup))
	text_file.close()

	return soup

def returnFirst(links):
	for link in links:
		url = link.string
		article = Article(url)

		article.download()
		article.parse()
		if (len(article.text) > 1000):
			# print(article.text)
			return article

def specificArticle(name, firstArticle):
	soup = BeautifulSoup(firstArticle.html, 'html.parser')

	open('nofilter.html', 'w').close()
	text_file = open("nofilter.html", "w")
	text_file.write(str(soup))
	text_file.close()

	if (name == 'stratechery'):
		return soup.find('article')
	elif (name == 'startupboy'):
		return soup.find('article')
	elif (name == 'overcoming_bias'):
		return soup.find("div", id="content")
	elif (name =='marginal_revolution'):
		return soup.find('article')
	elif (name =='bryan_caplan_econlib'):
		return soup.find('article')
	elif (name=='ribbonfarm'):
		return soup.find_all("div", class_="type-post")[0]
	else:
		return soup	

def cleanTags(soup):
	REMOVE_TAG = ['head', 'script', 'form', 'input', 'button']

	for tag in REMOVE_TAG:
		for e in soup.findAll(tag):
			e.extract()

	return soup

def cleanAttributes(soup):
	SAVE_ATTRIBUTES = ['href', 'src']
	SAVE_TAG = ['img']
	for tag in soup.recursiveChildGenerator():
		if tag.name not in SAVE_TAG:
			try:
				key_list = list( tag.attrs.keys() )
				for key in key_list:
					if key not in SAVE_ATTRIBUTES:
						del tag.attrs[key]
			except AttributeError: 
	        # 'NavigableString' object has no attribute 'attrs'
				pass
	return soup