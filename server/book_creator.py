import shutil
import os
from bs4 import BeautifulSoup
import json

def createEBook(name):
	convertToXHTML()
	shutil.rmtree('./publishing')
	os.mkdir('./publishing')
	shutil.make_archive('./publishing/' + name , 'zip', './EPUB_Template')
	os.rename('./publishing/' + name + '.zip', './publishing/' + name + '.epub')

def convertToXHTML():
	open('a.xml', 'w').close()
	f = open('output.html')
	soup = BeautifulSoup(f, features="lxml")
	f.close()
	g = open('a.xml', 'w')
	g.write(str(soup))
	g.close()
	injectXML()

def injectXML():
	f = open('a.xml', "r")
	contents = f.read()
	bookSoup = BeautifulSoup(contents, "xml")
	innerbody = bookSoup.body.findChildren()[0]

	page = open('./EPUB_Template/OEBPS/Text/chap01.xhtml')
	soup = BeautifulSoup(page, features="lxml")
	page.close()
	open('./EPUB_Template/OEBPS/Text/chap01.xhtml', 'w').close()
	elem = soup.find('body')
	elem.clear()
	elem.append(innerbody)
	page = open('./EPUB_Template/OEBPS/Text/chap01.xhtml', "w")
	page.write(str(soup))
	page.close()




