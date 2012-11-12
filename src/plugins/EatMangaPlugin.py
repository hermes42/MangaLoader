#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib
import urllib2
import logging
from HTMLParser import HTMLParser

import src.PluginBase as PluginBase

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('EatMangaPlugin')

# -------------------------------------------------------------------------------------------------
#  Plugin class
# -------------------------------------------------------------------------------------------------
class EatMangaPlugin(PluginBase.PluginBase):

	def __init__(self):
		self.__domain = "http://eatmanga.com/Manga-Scan"
	
	def getImage(self, image):
		global logger
		
		manga = image.chapter.manga
		chapter = image.chapter
		
		# http://eatmanga.com/Manga-Scan/Hellsing/Hellsing-002/page-2
		url = self.__domain + "/" + self.__getInternalName(manga.name) + "/" + self.__getInternalName(manga.name) + "-" + ("%03d" % chapter.chapterNo) + "/page-" + str(image.imageNo)
		result = PluginBase.loadURL(url)
		
		logger.debug("start parsing")
		parser = EatMangaParser()
		parser.feed(result)
		
		logger.debug("targetCount = " + str(parser.targetCount))
		if parser.targetCount < 1:
			logger.info("No image found in MangaReader site, maybe the chapter is not available.")
			return False
		
		if parser.targetCount > 1:
			logger.warning(str(parser.targetCount) + " images found in MangaReader site, maybe the chapter is not available.")
			return False
		
		if parser.targetValue == "":
			logger.warning("No valid image url found in MangaReader site.")
			return False
		
		# TODO how to find out if the manga/chapter is over? (after a chapter no valid image file is returned)
		if str(parser.targetValue).endswith("/"):
			logger.warning("No valid image url found in MangaReader site, maybe the the chapter is over.")
			return False
		
		logger.debug("imageURL = " + str(parser.targetValue))
		image.imageUrl = parser.targetValue
		logger.debug("imageUrl found: " + parser.targetValue)
		return True
	
	
	def __getInternalName(self, name):
		internalName = name
		# TODO check what to do here
		return internalName



class EatMangaParser(HTMLParser):
	
	def __init__(self):
		"""Constructor"""
		HTMLParser.__init__(self)
		
		self.targetValue = ""
		self.targetCount = 0
	
	def handle_starttag(self, tag, attrs):
		"""Handle HTML start tags"""
		global logger
		
		# TODO use eatmanga_image or eatmanga_image_big?
		if self.isImageTag(tag, attrs):
			for attr in attrs:
				if (attr[0] == "src"):
					logger.debug("imageURL found")
					self.targetValue = attr[1]
					self.targetCount = self.targetCount + 1
					break
	
	def handle_data(self, data):
		"""Handle HTML data"""
		pass
	
	def handle_endtag(self, tag):
		"""Handle HTML end tags"""
		pass
	
	def handle_data(self, data):
		"""Handle HTML data"""
		pass
	
	
	def isImageTag(self, tag, attrs):
		global logger
		
		if tag == "img":
			for attr in attrs:
				if attr[0] == "id":
					if attr[1] == "eatmanga_image":
						logger.debug("\"eatmanga_image\" found")
						return True
					if attr[1] == "eatmanga_image_big":
						logger.debug("\"eatmanga_image_big\" found")
						return True
		return False



# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	print "no test implemented"



