import shutil
import os
from bs4 import BeautifulSoup

def createEBook():
	convertToXHTML()
	os.remove('./publishing/archive.epub')
	shutil.make_archive('./publishing/archive', 'zip', './EPUB_Template')
	os.rename('./publishing/archive.zip', './publishing/archive.epub')

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
	innerbody = bookSoup.find('body')

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




