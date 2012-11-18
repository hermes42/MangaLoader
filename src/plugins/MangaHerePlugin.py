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

logger = logging.getLogger('MangaHerePlugin')

# TODO implement volume support (e.g. http://www.mangahere.com/manga/naruto/v60/c600/ - volume 60)

# -------------------------------------------------------------------------------------------------
#  Module class
# -------------------------------------------------------------------------------------------------
class MangaHerePlugin(PluginBase.PluginBase):

	def __init__(self):
		self.__domain = "http://www.mangahere.com/manga"
	
	def getImage(self, image):
		global logger
		
		manga = image.chapter.manga
		chapter = image.chapter
		
		url = self.__domain + "/" + self.__getInternalName(manga.name) + "/c" + ("%03d" % chapter.chapterNo) + "/" + str(image.imageNo) + ".html"
		result = PluginBase.loadURL(url)
		
		if result is None:
			return False
		
		logger.debug("start parsing")
		parser = PluginBase.ParserBase(("section", "id", "viewer"), ("img", "src"))
		parser.feed(result)
		
		logger.debug("targetCount = " + str(parser.targetCount))
		if parser.targetCount < 1:
			logger.info("No image found in MangaHere site, maybe the chapter is not available.")
			return False
		
		if parser.targetCount > 1:
			logger.warning(str(parser.targetCount) + " images found in MangaHere site, maybe the chapter is not available.")
			return False
		
		if parser.targetValue == "":
			logger.warning("No valid image url found in MangaHere site.")
			return False
		
		logger.debug("imageURL = " + str(parser.targetValue))
		image.imageUrl = parser.targetValue
		logger.debug("imageUrl found: " + parser.targetValue)
		return True
	
	
	def __getInternalName(self, name):
		internalName = name
		internalName = str.lower(internalName)
		internalName = str.replace(internalName, " ", "-")
		return internalName



# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	print "no test implemented"



