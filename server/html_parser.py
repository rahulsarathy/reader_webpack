from bs4 import BeautifulSoup
from newspaper import Article
from urllib.request import urlopen
from urllib.request import Request as req
import os


# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>

# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>

# <p class="story">...</p>
# """

# soup = BeautifulSoup(html_doc, 'html.parser')

def parseHTML(html):
	soup = BeautifulSoup(html, 'html.parser')
	output = soup.get_text()
	print("output is " + output)
	return output

# def parseStratechery():
def findFirst():
	url = request.values.get('url')
	# url = 'https://stratechery.com/feed'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	soup = BeautifulSoup(xml, 'xml')
	links = soup.find_all('guid')
	# print(links)
	firstArticle = returnFirst(links)
	html = firstArticle.html

	r = Response(html, status=200)
	return r

#find the first link that is not too short
def returnFirst(links):
	for link in links:
		url = link.string
		article = Article(url)

		article.download()
		article.parse()
		if (len(article.text) > 1000):
			print(article.text)
			return article

def correct():
	url = "http://www.overcomingbias.com/feed"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	toSend = req(url=url, headers=headers)
	xml = urlopen(toSend).read()
	soup = BeautifulSoup(xml, 'html.parser')
	# rss_feed = soup.find('content:encoded')
	rss_feed = soup.find('item')

	open("testing.html", 'w').close()
	text_file = open("testing.html", "w")
	text_file.write(str(rss_feed))


def main():
	correct()

if __name__ == '__main__':
	main()
