#!/usr/bin/python3

import os
import logging
import mimetypes
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

import requests

from . import MangaZipper

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaLoader.MangaBase')

MAX_DOWNLOAD_WORKER = 1


# -------------------------------------------------------------------------------------------------
#  Manga class
# -------------------------------------------------------------------------------------------------
class Manga(object):

    def __init__(self, name):
        self.name = name
        self.chapterList = []
        self.mangaURL = ''
        self.internalName = ''

    def __str__(self):
        return str(self.name)

    def addChapter(self, chapter):
        chapter.manga = self
        self.chapterList.append(chapter)


# -------------------------------------------------------------------------------------------------
#  Chapter class
# -------------------------------------------------------------------------------------------------
class Chapter(object):

    def __init__(self, manga, chapterNo):
        self.manga = manga
        self.chapterNo = chapterNo
        self.chapterTitle = ''
        self.chapterURL = ''
        self.imageList = []

    def __str__(self):
        if self.manga != None:
            return str(self.manga) + ' ' + str(self.chapterNo)
        else:
            return str(self.chapterNo)

    def addImage(self, image):
        image.chapter = self
        self.imageList.append(image)


# -------------------------------------------------------------------------------------------------
#  Image class
# -------------------------------------------------------------------------------------------------
class Image(object):

    def __init__(self, chapter, imageNo):
        self.chapter = chapter
        self.imageNo = imageNo
        self.imageURL = None

    def __str__(self):
        if self.chapter != None:
            return str(self.chapter) + ' - ' + str(self.imageNo)
        else:
            return str(self.imageNo)


# -------------------------------------------------------------------------------------------------
#  Loader class
# -------------------------------------------------------------------------------------------------
class Loader(object):

    def __init__(self, loaderPlugin, destDir):
        self.loaderPlugin = loaderPlugin
        self.destDir = destDir

    def handleChapter2(self, chapter):
        logger.debug('handleChapter({})'.format(chapter))
        if self.parseChapter(chapter) == False:
            return False
        if self.loadChapter(chapter) == False:
            return False
        return True

    def handleChapter(self, name, chapterNo):
        logger.debug('handleChapter({}, {})'.format(name, chapterNo))
        chapter = Chapter(Manga(name), chapterNo)
        if self.parseChapter(chapter) == False:
            return False
        if self.loadChapter(chapter) == False:
            return False
        return True

    def handleImage(self, name, chapterNo, imageNo):
        logger.debug('handleChapter({}, {}, {})'.format(name, chapterNo, imageNo))
        image = Image(Chapter(Manga(name), chapterNo), imageNo)
        if self.parseImage(image) == False:
            return False
        if self.loadImage(image) == False:
            return False
        return True

    def zipChapter(self, name, chapterNo):
        logger.debug('zipChapter({}, {})'.format(name, chapterNo))
        manga = Manga(name)
        chapter = Chapter(manga, chapterNo)
        if MangaZipper.createZip(self.getChapterDir(chapter), self.getMangaDir(manga)):
            logger.info('cbz: "' + str(chapter) + '"')
            print('cbz: "' + str(chapter) + '"')
            return True
        return False

    def zipChapter2(self, manga, chapter):
        logger.debug('zipChapter({}, {})'.format(manga.name, chapter.chapterNo))
        if MangaZipper.createZip(self.getChapterDir(chapter), self.getMangaDir(manga)):
            logger.info('cbz: "' + str(chapter) + '"')
            print('cbz: "' + str(chapter) + '"')
            return True
        return False

    def parseManga(self, manga):
        retValue = False
        # FIXME Do NOT use maximum number of chapters because "One Piece" :-)
        for i in range(1, 1000):
            chapter = Chapter(manga, i)
            if self.parseChapter(chapter) == False:
                break
            manga.addChapter(chapter)
            retValue = True
        return retValue

    def parseChapter(self, chapter):
        retValue = False
        for i in range(1,1000):
            image = Image(chapter, i)
            if self.parseImage(image) == False:
                break
            chapter.addImage(image)
            retValue = True
        return retValue

    def parseImage(self, image):
        if self.loaderPlugin == None:
            return False
        if self.loaderPlugin.getImage(image) == False:
            return False

        logger.info('parse: "' + str(image) + '"')
        print('parse: "' + str(image) + '"')
        return True

    def loadManga(self, manga):
        for chapter in manga.chapterList:
            if self.loadChapter(chapter) == False:
                return False
        return True

    def loadChapter(self, chapter):
        list_of_futures = list()
        # context manager cleans up automatically after all threads have executed 
        with ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKER) as executor:
            for image in chapter.imageList:
                f = executor.submit(self.loadImage, image)
                list_of_futures.append(f)
        return True

    def loadImage(self, image):       
        # calculate destination path and call storeFileOnDisk()
        if self.storeFileOnDisk(image.imageUrl, self.getImagePath(image)) == False:
            return False
        logger.info('load: "{}"'.format(image))
        print('load: "{}"'.format(image))
        return True

    def getMangaDir(self, manga):
        if type(manga) == Manga:
            return os.path.join(self.destDir, manga.name)
        elif type(manga) == str:
            return os.path.join(self.destDir, manga)
        else:
            logger.error('Wrong type of parameter "manga"!')

    def getChapterDir(self, chapter):
        return os.path.join(self.getMangaDir(chapter.manga), '{} {}'.format(chapter.manga, chapter.chapterNo))

    def getImagePath(self, image):
        """
        Builds the path to save the downloaded image to. It contains no file
        extension, because it is later added depending on the header
        information of the HTTP response.
        """
        imageExtension = '' # '.' + os.path.splitext(image.imageUrl)
        return os.path.join(self.getChapterDir(image.chapter),
                            '{ImageNo:03d}{Ext}'.format(ImageNo=image.imageNo,Ext=imageExtension))

    def storeFileOnDisk(self, source, dest):
        # create directories first
        try:
            os.makedirs(dest[0 : dest.rfind('/')])
        except OSError:
            pass
        # open source url and copy to destination file; retry 5 times
        # TODO: Check how to implement retry counter with requests library.
        tryCounter = 1
        while True:
            try:
                r = requests.get(source, stream=True)
                # get file extension for content type
                content_type = r.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                # alternatively use urllib to parse url to get extension
                parsed = urlparse(source)
                root, ext = os.path.splitext(parsed.path)
                if extension != ext:
                    logger.warn('File extension unclear: {} <-> {}'.format(extension, ext))
                # save data to file if status code 200 was returned
                if r.status_code == 200:
                    with open(dest+extension, 'wb') as f:
                        # write chunks of default size (128 byte)
                        for chunk in r:
                            f.write(chunk)
                self.loaderPlugin.postprocessImage(dest)
                return True
            except urllib.error.URLError:
                logger.warning('failed to load "' + str(source) + '" (' + tryCounter + ')')
                if tryCounter >= 5:
                    logger.error('failed to load "' + str(source) + '"')
                    return False
            tryCounter = tryCounter + 1
        return False


# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('No test implemented!')
