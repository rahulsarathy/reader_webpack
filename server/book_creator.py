import shutil
import os
from bs4 import BeautifulSoup

def createEBook():
	convertToXHTML()
	os.remove('archive.epub')
	shutil.make_archive('archive', 'zip', './EPUB_Template')
	os.rename('archive.zip', 'archive.epub')

def convertToXHTML():
	open('a.xml', 'w').close()
	f = open('output.html')
	soup = BeautifulSoup(f, features="lxml")
	f.close()
	g = open('a.xml', 'w')
	g.write(str(soup))
	g.close()