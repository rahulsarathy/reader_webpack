from newspaper import Article
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request as req
import pickle
import time

def findFirst(name, xml):
	# url = 'https://stratechery.com/feed'
	link = xml.find('guid').text

	article = Article(link)
	article.download()
	article.parse()

	#clean html
	soup = specificArticle(name, article)
	soup = cleanTags(soup)
	soup = cleanAttributes(soup)

	return soup

def specificArticle(name, firstArticle):
	soup = BeautifulSoup(firstArticle.html, 'html.parser')

	if (name=='ribbonfarm'):
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