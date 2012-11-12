#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib
import urllib2
import logging
from HTMLParser import HTMLParser

import MangaBase

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaReader')

# -------------------------------------------------------------------------------------------------
#  Module class
# -------------------------------------------------------------------------------------------------
class Module(object):

	def __init__(self):
		self.domain = "http://www.mangareader.net"
	
	def getImage(self, image):
		global logger
		
		manga = image.chapter.manga
		chapter = image.chapter
		
		url = self.domain + "/" + self.getInternalName(manga.name) + "/" + str(chapter.chapterNo) + "/" + str(image.imageNo)
		
		tryCounter = 1
		while True:
			
			logger.debug("start loading image \"" + str(image) + "\"")
			try:
				headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0" }
				request = urllib2.Request(url, None, headers)
				
				response = urllib2.urlopen(request)
				result = response.read()
				break
			except urllib2.URLError, e:
				logger.debug("URLError: " + str(e))
				if tryCounter >= 5:
					return False
			tryCounter = tryCounter + 1
		
		logger.debug("start parsing")
		parser = Parser()
		parser.feed(result)
		
		logger.debug("imageCount = " + str(parser.imageCount))
		if parser.imageCount < 1:
			# TODO logger.info("No image found in MangaReader site, maybe the chapter is not available.")
			return False
		
		if parser.imageCount > 1:
			# TODO logger.info(str(parser.imageCount) + " images found in MangaReader site, maybe the chapter is not available.")
			return False
		
		if parser.imageUrl == "":
			# TODO logger.warning("No valid image url found in MangaReader site.")
			return False
		
		logger.debug("imageURL = " + str(parser.imageUrl))
		image.imageUrl = parser.imageUrl
		# TODO logger.info("imageUrl found: " + parser.imageUrl)
		return True
	
	
	def getInternalName(self, name):
		internalName = name
		internalName = str.lower(internalName)
		internalName = str.replace(internalName, " ", "-")
		return internalName


# -------------------------------------------------------------------------------------------------
#  Parser class
# -------------------------------------------------------------------------------------------------
class Parser(HTMLParser):
  
	"""Constructor"""
	def __init__(self):
		HTMLParser.__init__(self)
		
		self.imageUrl = ""
		self.imageCount = 0
		self.insideImageTag = False
		self.divCount = 0
	
	"""Handle HTML start tags"""
	def handle_starttag(self, tag, attrs):
		if self.insideImageTag:
			self.increaseDivCount(tag)
			self.loadImageHolder(tag, attrs)
		else:
			self.findImageHolderStart(tag, attrs)
	
	"""Handle HTML data"""
	def handle_data(self, data):
		pass
	
	"""Handle HTML end tags"""
	def handle_endtag(self, tag):
		if self.insideImageTag:
			self.decreaseDivCount(tag)
	
	"""Handle HTML data"""
	def handle_data(self, data):
		pass
	
	
	"""Check whether the current tag contains the image holder."""
	def findImageHolderStart(self, tag, attrs):
		# find image holder div
		
		global logger
		
		if tag == "div":
			for attr in attrs:
				if (attr[0] == "id") and (attr[1] == "imgholder"):
					logger.debug("imgholder div start")
					self.insideImageTag = True
					self.divCount = 1
					break
	
	def increaseDivCount(self, tag):
		if tag == "div":
			self.divCount = self.divCount + 1
	
	def decreaseDivCount(self, tag):
		global logger
		logger.debug("decreaseDivCount(" + str(tag) +")")
		if tag == "div":
			self.divCount = self.divCount - 1
		if self.divCount == 0:
			logger.debug("imgholder div end")
			self.insideImageTag = False
	
		"""Try to load the imageUrl from image holder."""
	def loadImageHolder(self, tag, attrs):
		# find image inside of image holder
		global logger
		if self.insideImageTag:
			if tag == "img":
				for attr in attrs:
					if attr[0] == "src":
						logger.debug("img.src found")
						self.imageUrl = attr[1]
						self.imageCount = self.imageCount + 1
						break



# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	print "no test implemented"



