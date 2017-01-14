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
    logger.debug('createZip(' + str(mangaDir) + ', ' + str(destDir) + ')')

    if not os.path.exists(mangaDir):
        return False

    name = os.path.basename(os.path.dirname(mangaDir))
    zipFileName = name + '.cbz'
    logger.debug('create cbz file "{}"...'.format(str(zipFileName)))
    cbzFile = zipfile.ZipFile(destDir + '/' + zipFileName, 'w')

    for f in os.listdir(mangaDir):
        # TODO check file extension
        #  fileName, fileExtension = os.path.splitext(f)
        logger.debug('add file "{}" to cbz file "{}".'.format(str(f), str(zipFileName)))
        cbzFile.write(mangaDir + '/' + f, name + '/' + os.path.basename(f).encode('ascii'), zipfile.ZIP_DEFLATED)

    return True

# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print('No test implemented!')
