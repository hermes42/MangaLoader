#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import src.PluginBase as PluginBase

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaReaderPlugin')

# -------------------------------------------------------------------------------------------------
#  Plugin class
# -------------------------------------------------------------------------------------------------
class MangaReaderPlugin(PluginBase.PluginBase):

	def __init__(self):
		self.__domain = "http://www.mangareader.net"
	
	def getImage(self, image):
		global logger
		
		manga = image.chapter.manga
		chapter = image.chapter
		
		url = self.__domain + "/" + self.__getInternalName(manga.name) + "/" + str(chapter.chapterNo) + "/" + str(image.imageNo)
		result = PluginBase.loadURL(url)
		
		if result is None:
			return False
		
		logger.debug("start parsing")
		parser = PluginBase.ParserBase(("div", "id", "imgholder"), ("img", "src"))
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
	print("no test implemented")
