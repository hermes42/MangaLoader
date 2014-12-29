#!/usr/bin/python3

import os
import urllib.request, urllib.error, urllib.parse
import logging
from string import Template
from concurrent.futures import ThreadPoolExecutor

from . import MangaZipper

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaLoader.MangaBase')

MAX_DOWNLOAD_WORKER = 2


# -------------------------------------------------------------------------------------------------
#  Manga class
# -------------------------------------------------------------------------------------------------
class Manga(object):

    def __init__(self, name):
        self.name = name
        self.chapterList = []
        self.mangaURL = ''

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

    def handleChapter(self, name, chapterNo):
        global logger
        logger.debug('handleChapter({}, {})'.format(str(name), str(chapterNo)))
        chapter = Chapter(Manga(name), chapterNo)

        if self.parseChapter(chapter) == False:
            return False

        if self.loadChapter(chapter) == False:
            return False

        return True

    def handleImage(self, name, chapterNo, imageNo):
        global logger
        logger.debug('handleChapter({}, {}, {})'.format(str(name), str(chapterNo), str(imageNo)))
        image = Image(Chapter(Manga(name), chapterNo), imageNo)

        if self.parseImage(image) == False:
            return False

        if self.loadImage(image) == False:
            return False

        return True

    def zipChapter(self, name, chapterNo):
        global logger
        logger.debug('zipChapter({}, {})'.format(str(name), str(chapterNo)))

        manga = Manga(name)
        chapter = Chapter(manga, chapterNo)
        if MangaZipper.createZip(self.getChapterDir(chapter), self.getMangaDir(manga)):
            logger.info('cbz: "' + str(chapter) + '"')
            print('cbz: "' + str(chapter) + '"')
            return True

        return False


    def parseManga(self, manga):
        retValue = False
        for i in range(1,1000):
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
        global logger

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
        with ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKER) as executor:
            for image in chapter.imageList:
                f = executor.submit(self.loadImage, image)
                list_of_futures.append(f)
        return all(list_of_futures)

    def loadImage(self, image):
        global logger

        # calculate destination path and call loadFile
        if self.loadFile(image.imageUrl, self.getImagePath(image)) == False:
            return False

        logger.info('load: "' + str(image) + '"')
        print('load: "' + str(image) + '"')
        return True


    def getMangaDir(self, manga):
        return Template(self.destDir + '/${MangaName}/').substitute(MangaName=manga.name)

    def getChapterDir(self, chapter):
        return Template(self.getMangaDir(chapter.manga) + '${MangaName} ${ChapterNo}/').substitute(MangaName=chapter.manga.name, ChapterNo=chapter.chapterNo)

    def getImagePath(self, image):
        return Template(self.getChapterDir(image.chapter) + '${ImageNo}.${Ext}').substitute(ImageNo=str(image.imageNo).rjust(2, '0'), Ext=image.imageUrl[image.imageUrl.rfind('.') + 1 : len(image.imageUrl)])

    def loadFile(self, source, dest):
        global logger

        # create directories first
        try:
            os.makedirs(dest[0 : dest.rfind('/')])
        except OSError:
            pass

        # open source url and copy to destination file
        # retry 5 times
        tryCounter = 1
        while True:
            try:
                f = urllib.request.urlopen(source)
                out = open(dest,'wb')
                out.write(f.read())
                out.close()
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
