#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib
import urllib2
import logging
from HTMLParser import HTMLParser

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('PluginBase')

# -------------------------------------------------------------------------------------------------
#  Parser class
# -------------------------------------------------------------------------------------------------
class PluginBase(object):
	
	def getImage(self, image):
		pass

# -------------------------------------------------------------------------------------------------
#  Parser class
# -------------------------------------------------------------------------------------------------
class ParserBase(HTMLParser):
	
	# TODO extend to a list of (tags, attrib, value) tupel, to find a specific value? [("div", "id", "imgholder"), ("img", "src", xxx)]
	
	def __init__(self, outer, inner):
		"""Constructor"""
		HTMLParser.__init__(self)
		
		(outerTag, outerAttrib, outerValue) = outer
		(innerTag, innerAttrib) = inner
		
		self.__outerTag = outerTag
		self.__outerAttrib = outerAttrib
		self.__outerValue = outerValue
		self.__innerTag = innerTag
		self.__innerAttrib = innerAttrib
		
		self.__insideOuterTag = False
		self.__outerCount = 0
		
		self.targetValue = ""
		self.targetCount = 0
	
	def handle_starttag(self, tag, attrs):
		"""Handle HTML start tags"""
		self.findOuterTagStart(tag, attrs)
		if self.__insideOuterTag:
			self.increaseOuterCount(tag)
			self.findInnerTag(tag, attrs)
	
	def handle_data(self, data):
		"""Handle HTML data"""
		pass
	
	def handle_endtag(self, tag):
		"""Handle HTML end tags"""
		if self.__insideOuterTag:
			self.decreaseOuterCount(tag)
	
	def handle_data(self, data):
		"""Handle HTML data"""
		pass
	
	
	def findOuterTagStart(self, tag, attrs):
		"""Check whether the current tag is the outer tag to search for."""
		global logger
		
		if tag == self.__outerTag:
			for attr in attrs:
				if (attr[0] == self.__outerAttrib) and (attr[1] == self.__outerValue):
					logger.debug("outer tag start")
					self.__insideOuterTag = True
					break
	
	def increaseOuterCount(self, tag):
		"""Increases the current level of outer tags inside the outer tag."""
		if tag == self.__outerTag:
			self.__outerCount = self.__outerCount + 1
	
	def decreaseOuterCount(self, tag):
		"""Decreases the current level of outer tags inside the outer tag. If the count reaches zero, this is the outer end tag."""
		if tag == self.__outerTag:
			self.__outerCount = self.__outerCount - 1
		if self.__outerCount == 0:
			logger.debug("outer tag end")
			self.__insideOuterTag = False
	
	def findInnerTag(self, tag, attrs):
		"""Check whether the current tag is the inner tag to search for."""
		global logger
		if self.__insideOuterTag:
			if tag == self.__innerTag:
				for attr in attrs:
					if attr[0] == self.__innerAttrib:
						logger.debug("inner value found")
						self.targetValue = attr[1]
						self.targetCount = self.targetCount + 1
						break


# -------------------------------------------------------------------------------------------------
#  loadURL
# -------------------------------------------------------------------------------------------------
def loadURL(url, maxTryCount=5):
	global logger
	
	tryCounter = 1
	while True:
		
		logger.debug("start loading URL \"" + str(url) + "\"")
		try:
			headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0" }
			request = urllib2.Request(url, None, headers)
			
			response = urllib2.urlopen(request)
			result = response.read()
			
			logger.debug("URL successfully loaded")
			return result
		except urllib2.URLError, e:
			logger.debug("URLError: " + str(e))
			if tryCounter >= maxTryCount:
				return None
		tryCounter = tryCounter + 1
	
	return None



# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	print "no test implemented"



