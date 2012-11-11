#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import glob
import zipfile
import logging

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaZipper')

# -------------------------------------------------------------------------------------------------
#  zipper functions
# -------------------------------------------------------------------------------------------------
def createZip(mangaDir, destDir):
	global logger
	logger.debug("createZip(" + str(mangaDir) + ", " + str(destDir) + ")")
	
	name = os.path.basename(os.path.dirname(mangaDir))
	zipFileName = name + ".cbz"
	logger.debug("create cbz file \"" + str(zipFileName) + "\"")
	cbzFile = zipfile.ZipFile(destDir + "/" + zipFileName, "w")
	
	for f in os.listdir(mangaDir):
		# TODO check file extension
		#  fileName, fileExtension = os.path.splitext(f)
		logger.debug("add file \"" + str(f) + "\" to cbz file \"" + str(zipFileName) + "\"")
		cbzFile.write(mangaDir + "/" + f, name + "/" + os.path.basename(f).encode("ascii"), zipfile.ZIP_DEFLATED)

# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	print "no test implemented"


# TODO implement me
