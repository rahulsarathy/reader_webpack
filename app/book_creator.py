import shutil, errno
from shutil import copyfile
import os
from bs4 import BeautifulSoup
import json

def createEBook(name):
	copyanything('./EPUB_Template', './publishing/construction/' + name + '/')
	convertToXHTML(name)
	copyfile("./publishing/images/" + name + "/author.jpg", './publishing/construction/' + name + '/OEBPS/images/author.jpg')
	copyfile("./publishing/images/" + name + "/cover.jpg", './publishing/construction/' + name + '/OEBPS/images/cover.jpg')

	shutil.make_archive('./publishing/books/' + name , 'zip', './publishing/construction/' + name + '/')
	os.rename('./publishing/books/' + name + '.zip', './publishing/books/' + name + '.epub')
	shutil.rmtree('./publishing/construction/' + name + '/')

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
	page = open('./publishing/construction/' + name + '/OEBPS/Text/chap01.xhtml')
	soup = BeautifulSoup(page, features="lxml")
	page.close()
	open('./publishing/construction/' + name + '/OEBPS/Text/chap01.xhtml', 'w').close()
	elem = soup.find('body')
	elem.clear()
	elem.append(bookSoup)
	page = open('./publishing/construction/' + name + '/OEBPS/Text/chap01.xhtml', "w")
	page.write(str(soup))
	page.close()

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

