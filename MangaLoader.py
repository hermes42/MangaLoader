#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
from optparse import OptionParser

import src.MangaBase as MangaBase
import src.plugins.MangaReaderPlugin as MangaReaderPlugin
import src.plugins.MangaHerePlugin as MangaHerePlugin
import src.plugins.EatMangaPlugin as EatMangaPlugin

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger("MangaLoader")

DATA_DIR = os.getenv("HOME") + "/.MangaLoader"
LOG_FORMAT = "%(asctime)-23s [%(levelname)8s] %(name)-15s %(message)s (%(filename)s:%(lineno)s)"
LOG_LEVEL = logging.DEBUG

class LogHelper(object):

	def __enter__(self):
		global logger
		global DATA_DIR
		global LOG_FORMAT
		global LOG_LEVEL
		
		try:
			os.makedirs(DATA_DIR)
		except OSError:
			pass
		
		self.fd = open(DATA_DIR + "/log", "a")
		logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, stream=self.fd)
		
		logger.info("logger initialized")
	
	def __exit__(self, type, value, traceback):
		global logger
		
		logger.info("deinitializing logger")
		
		self.fd.flush()
		self.fd.close()


# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------

# test with:
#  python MangaLoader.py -m -n Claymore -r 14 20 -o /home/markus/Desktop/New Mangas

with LogHelper() as l:
	
	"""
	specify options and parse arguments
	"""
	
	logger.info("MangaLoader started")
	
	logger.debug("starting to parse options and args")
	
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option("--version",
					action="store_true",
					dest="version",
					help="show version information")
	parser.add_option("--MangaReader",
					action="store_true",
					dest="MangaReader",
					help="use MangaReader plugin")
	parser.add_option("--MangaHere",
					action="store_true",
					dest="MangaHere",
					help="use MangaHere plugin")
	parser.add_option("--EatManga",
					action="store_true",
					dest="EatManga",
					help="use EatManga plugin")
	parser.add_option("-z",
					action="store_true",
					dest="Zip",
					help="create cbz files")
	parser.add_option("-n",
					action="store",
					type="string",
					dest="name",
					metavar="NAME",
					help="name of the manga")
	parser.add_option("-r",
					action="store",
					type="int",
					dest="range",
					nargs=2,
					metavar="FROM TO",
					help="load a range of chapters")
	parser.add_option("-i",
					action="store",
					type="int",
					dest="image",
					nargs=2,
					metavar="CHAPTER IMAGE",
					help="load a single image (chapterNo, imageNo)")
	parser.add_option("-o",
					action="store",
					type="string",
					dest="output",
					metavar="DEST_DIR",
					help="destination directory")
	
	(options, args) = parser.parse_args()
	
	if options.version != None:
		print "MangaLoader v0.1 alpha"
		sys.exit()
	
	if options.name is None:
		logger.error("no manga name specified")
		print "Missing manga name."
		sys.exit()
	
	if options.output is None:
		logger.error("no dest dir specified")
		print "Missing destination folder."
		sys.exit()
	
	if (options.range is None) and (options.image is None):
		logger.error("neither range nor image option specified")
		print "Specify at least range of images."
		sys.exit()
	
	pluginCount = 0
	if (options.MangaReader is not None):
		pluginCount = pluginCount + 1
	if (options.MangaHere is not None):
		pluginCount = pluginCount + 1
	if (options.EatManga is not None):
		pluginCount = pluginCount + 1
	
	if  pluginCount <= 0:
		logger.error("no plugin selected")
		print "Specify exactly one plugin."
		sys.exit()
	if  pluginCount > 1:
		logger.error("multiple plugins selected")
		print "Specify exactly one plugin."
		sys.exit()
	
	logger.debug("options parse done")
	
	
	
	"""
	start actual manga load with specified parameter & arguments
	"""
	
	start_time = time.time()
	logger.debug("start time: %.2f s" %(start_time))
	
	mangaName = options.name
	destDir = options.output
	
	if options.range is not None:
		useRange = True
		startChapter = options.range[0]
		endChapter = options.range[1]
	else:
		useRange = False
		chapter = options.image[0]
		image = options.image[1]
	
	doZip = options.Zip != None
	
	logger.info("loading plugin")
	if options.MangaReader is not None:
		plugin = MangaReaderPlugin.MangaReaderPlugin()
		logger.debug("using MangaLoader plugin")
	elif options.MangaHere is not None:
		plugin = MangaHerePlugin.MangaHerePlugin()
		logger.debug("using MangaHere plugin")
	elif options.EatManga is not None:
		plugin = EatMangaPlugin.EatMangaPlugin()
		logger.debug("using EatManga plugin")
	
	logger.info("loading Loader")
	loader = MangaBase.Loader(plugin, destDir)
	
	if useRange:
		logger.info("loading chapters " + str(startChapter) + " - " + str(endChapter))
		for i in xrange(startChapter, endChapter+1):
			loader.handleChapter(mangaName, i)
			if doZip:
				loader.zipChapter(mangaName, i)
	
	else:
		logger.info("loading image " + str(chapter) + " / " + str(image))
		loader.handleImage(mangaName, chapter, image)
		if doZip:
				loader.zipChapter(mangaName, chapter)
	
	end_time = time.time()
	logger.debug("end time: %.2f s" %(end_time))
	logger.info("elapsed time: %.2f s" %(end_time - start_time))
	print "Elapsed Time: %.2f s" %(end_time - start_time)
	
	logger.info("MangaLoader done")

