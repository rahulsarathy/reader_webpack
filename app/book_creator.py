import shutil, errno
from shutil import copyfile
import os
from bs4 import BeautifulSoup
import json
import urllib.request
from pathlib import Path

def createEBook(name):
	try:
		shutil.rmtree('./publishing/construction/' + name + '/')
	except OSError as e:
		print("nothing to delete for {}".format(name))
	copyanything('./EPUB_Template', './publishing/construction/' + name + '/')
	convertImages(name)
	convertToXHTML(name)
	if not os.path.exists('./publishing/construction/' + name + '/OEBPS/images/'):
		os.mkdir('./publishing/construction/' + name + '/OEBPS/images/')
	copyfile("./publishing/images/" + name + "/author.jpg", './publishing/construction/' + name + '/OEBPS/images/author.jpg')
	copyfile("./publishing/images/" + name + "/cover.jpg", './publishing/construction/' + name + '/OEBPS/images/cover.jpg')

	shutil.make_archive('./publishing/books/' + name , 'zip', './publishing/construction/' + name + '/')
	os.rename('./publishing/books/' + name + '.zip', './publishing/books/' + name + '.epub')
	shutil.rmtree('./publishing/construction/' + name + '/')

	cmd = './publishing/kindlegen ./publishing/books/' +  name + '.epub'
	os.system(cmd)

def convertImages(name):
	f = open('./publishing/html/' + name + '.html', 'r')
	soup = BeautifulSoup(f, 'html.parser')
	f.close()
	imgs = soup.findAll('img')
	for i in range(len(imgs)):
		print(imgs[i]['src'])

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib.request.install_opener(opener)
		if not os.path.exists('./publishing/construction/' + name + '/OEBPS/images/'):
			os.mkdir('./publishing/construction/' + name + '/OEBPS/images/')
		urllib.request.urlretrieve(imgs[i]['src'], './publishing/construction/' + name + '/OEBPS/images/image{}.png'.format(i))
		imgs[i]['src'] = '../Images/image{}.png'.format(i)
	f = open('./publishing/html/' + name + '.html', 'w')
	f.write(str(soup))
	f.close()


def convertToXHTML(name):
	f = open('./publishing/html/' + name + '.html', 'r')
	soup = BeautifulSoup(f, features="lxml")
	f.close()
	g = open('./publishing/xml/' + name + '.xml', 'w+')
	g.close()
	g = open('./publishing/xml/' + name + '.xml', 'w')
	g.write(str(soup))
	g.close()

	injectXML(name)

def createHTML(name, output):
	open( './publishing/html/' + name + '.html', 'w').close()
	text_file = open('./publishing/html/' + name + '.html', "w")
	text_file.write(str(output))
	text_file.close()

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

