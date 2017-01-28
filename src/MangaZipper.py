#!/usr/bin/python3

import os
import zipfile
import logging

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaLoader.MangaZipper')

# -------------------------------------------------------------------------------------------------
#  zipper functions
# -------------------------------------------------------------------------------------------------
def createZip(mangaDir, destDir):
    global logger
    logger.debug('createZip({}, {})'.format(mangaDir, destDir))

    if not os.path.exists(mangaDir) or not os.path.isdir(mangaDir):
        return False

    name = os.path.basename(os.path.normpath(mangaDir))
    zipFileName = name + '.cbz'
    logger.debug('create cbz file "{}"...'.format(zipFileName))
    cbzFile = zipfile.ZipFile(destDir + '/' + zipFileName, 'w')

    for f in os.listdir(mangaDir):
        # TODO check file extension
        #  fileName, fileExtension = os.path.splitext(f)
        logger.debug('add file "{}" to cbz file "{}".'.format(f, zipFileName))
        file_in_filesystem = os.path.join(mangaDir, f)
        file_in_zipfile = os.path.join(name, os.path.basename(f))
        cbzFile.write(file_in_filesystem, file_in_zipfile, zipfile.ZIP_DEFLATED)

    return True

# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print('No test implemented!')
