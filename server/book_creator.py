import shutil
import os
from bs4 import BeautifulSoup
import json

def createEBook(name):
	convertToXHTML(name)
	shutil.make_archive('./publishing/books/' + name , 'zip', './EPUB_Template')
	os.rename('./publishing/books/' + name + '.zip', './publishing/books/' + name + '.epub')

def convertToXHTML(name):
	f = open('./publishing/html/' + name + '.html', 'r')
	soup = BeautifulSoup(f, features="lxml")
	f.close()
	g = open('./publishing/xml/' + name + '.xml', 'w').close()
	g = open('./publishing/xml/' + name + '.xml', 'w')
	g.write(str(soup))
	g.close()

	injectXML(name)

def injectXML(name):
	f = open('./publishing/xml/' + name + '.xml', "r")
	contents = f.read()
	bookSoup = BeautifulSoup(contents, "xml")
	innerbody = bookSoup.body.findChildren()[0]

	page = open('./EPUB_Template/OEBPS/Text/chap01.xhtml')
	soup = BeautifulSoup(page, features="lxml")
	page.close()
	open('./EPUB_Template/OEBPS/Text/chap01.xhtml', 'w').close()
	elem = soup.find('body')
	elem.clear()
	elem.append(bookSoup)
	page = open('./EPUB_Template/OEBPS/Text/chap01.xhtml', "w")
	page.write(str(soup))
	page.close()



