#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import re
import logging
from html.parser import HTMLParser

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaLoader.PluginBase')

# -------------------------------------------------------------------------------------------------
#  Parser class
# -------------------------------------------------------------------------------------------------
class PluginBase():

    def getImage(self, image):
        """Gets an image URL for a specific manga from a specific chapter. The
        URL is stored in the given Image object.

        :return: whether a valid image URL could be found."""
        raise NotImplementedError()

    def getListOfChapters(self, manga):
        """Gets a list of all current chapters from a given manga.

        :param manga: identifier for a available manga on this site.
        :return: list of identifiers for all chapters of this manga currently
                 available at this site."""
        raise NotImplementedError()

    def getListOfMangas(self):
        """Gets the current list of all available mangas from a given site."""
        raise NotImplementedError()

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

        self.targetValue = ''
        self.targetCount = 0
        self.targetValues = list()
        self.targetData = list()

    def handle_starttag(self, tag, attrs):
        """Handle HTML start tags"""
        self.findOuterTagStart(tag, attrs)
        if self.__insideOuterTag:
            self.increaseOuterCount(tag)
            self.findInnerTag(tag, attrs)

    def handle_data(self, data):
        """Handles data only inside the given outer tag and stores the data
        each time in the same variable to be read."""
        if self.__insideOuterTag:
            if not data.isspace():
                self.targetData.append(data)

    def handle_endtag(self, tag):
        """Handle HTML end tags"""
        if self.__insideOuterTag:
            self.decreaseOuterCount(tag)

    def findOuterTagStart(self, tag, attrs):
        """Check whether the current tag is the outer tag to search for."""
        global logger

        if tag == self.__outerTag:
            # check attribute and its value only when they have been given...
            if self.__outerAttrib and self.__outerValue:
                for attr in attrs:
                    if (attr[0] == self.__outerAttrib) and (attr[1] == self.__outerValue):
                        logger.debug("outer tag start")
                        self.__insideOuterTag = True
                        break
            # ...otherwise just do it!
            else:
                logger.debug("outer tag start")
                self.__insideOuterTag = True

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
                        self.targetValues.append(attr[1])
                        self.targetCount = self.targetCount + 1
                        break


# -------------------------------------------------------------------------------------------------
#  loadURL
# -------------------------------------------------------------------------------------------------
def find_re_in_site(url, regex):
    """Opens a site, downloads its content and check with a regular expression
    whether any matching string can be found.
    
    :param url: site URL to be scanned for matching strings
    :param regex: regular expression to be searched for
    """
    site = urllib.request.urlopen(url)
    content = site.read().decode(site.headers.get_content_charset())
    list = re.findall(regex, content)
    return list


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
            request = urllib.request.Request(url, None, headers)

            response = urllib.request.urlopen(request)
            # read from URL and decode according to HTTP header info
            result = response.read().decode(response.headers.get_content_charset())

            logger.debug("URL successfully loaded")
            return result
        except urllib.error.URLError as e:
            logger.debug("URLError: " + str(e))
            if tryCounter >= maxTryCount:
                return None
        tryCounter = tryCounter + 1

    return None


# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("no test implemented")
