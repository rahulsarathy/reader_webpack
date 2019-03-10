import shutil
import os

def createEBook():
	os.remove('archive.epub')
	shutil.make_archive('archive', 'zip', './EPUB_Template')
	os.rename('archive.zip', 'archive.epub')