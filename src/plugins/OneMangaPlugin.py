#!/usr/bin/python3

import logging
import re
from itertools import islice

import src.PluginBase as PluginBase
from src.MangaBase import Manga
from src.MangaBase import Chapter
from src.helper import memoized


logger = logging.getLogger('MangaLoader.OneMangaPlugin')


BASE_URL = 'http://www.onemanga2.com'


# -------------------------------------------------------------------------------------------------
#  Plugin class
# -------------------------------------------------------------------------------------------------
class OneMangaPlugin(PluginBase.PluginBase):

    def __init__(self):
        self.__list_of_found_chapter_URLs = {}
        self.__last_found_image_URL = ''
        self.list_of_all_mangas = []

    def getImage(self, image):
        # http://www.onemanga2.com/Attack_on_Titan/61/30/
        # TODO Do not use raw data like chapter number and page number, use
        # link inside chapter object!
        manga = image.chapter.manga
        chapter = image.chapter

        if not chapter.chapterURL:
            # create URL from scratch only when it was not saved with the chapter
            url = '/'.join((BASE_URL, self.__getInternalName(manga),
                           str(chapter.chapterNo), str(image.imageNo)))
        else:
            # otherwise take given chapter URL and concatenate only page number
            url = chapter.chapterURL + str(image.imageNo)
        logger.debug('Parsing URL "{}" for manga page.'.format(url))
        result = PluginBase.loadURL(url)
        if result is None:
            return False

        logger.debug('Start parsing...')
        parser = PluginBase.FindTagParser('img', 'class', 'manga-page', 'src')
        parser.feed(result)

        logger.debug('targetCount = ' + str(parser.targetCount))
        if parser.targetCount < 1:
            logger.info('No image found in MangaReader site, maybe the chapter is not available.')
            return False
        if parser.targetCount > 1:
            logger.warning(str(parser.targetCount) + ' images found in MangaReader site, maybe the chapter is not available.')
            return False
        if parser.targetValue == '':
            logger.warning('No valid image url found in MangaReader site.')
            return False

        # check if this time the same URL was found as last time, because
        # MangaFox shows last image of chapter when the given image number is
        # too high
        # TODO: Fix this by determine how many chapters there are!
        if self.__last_found_image_URL == parser.targetValue:
            return False

        image.imageUrl = parser.targetValue
        self.__last_found_image_URL = parser.targetValue
        logger.debug('imageUrl found: {}'.format(parser.targetValue))

        return True

    def getListOfChapters(self, manga):
        url = manga.mangaURL
        logger.info('Looking for chapters of manga "{}" ({}).'.format(manga.name, manga.mangaURL))
        logger.info('Finding chapters...')
        result = PluginBase.loadURL(url)
        if result is None:
            return False
        parser = PluginBase.ParserBase(('ul', 'class', 'lst'), ('a', 'href'))
        parser.feed(result)
        list_of_chapters = []
        if parser.targetCount > 1:
            for number, link in enumerate(reversed(parser.targetValues), start=1):
                # values are iterated in reverse because we pop two values for
                # each link in the file and pop takes items from the other side
                date = parser.targetData.pop()
                title = parser.targetData.pop()
                # find chapter number if possible
                # 'Chapter 13' -> r'Chapter (/d+)'
                # FIXME Fix automatical detection of chapter numbers!
                x = re.findall('Chapter (\d+)', title)
                print(x)
                if x:
                    number = int(x[0])
                # build chapter object and save it in list
                chapter = Chapter(manga.name, number)
                chapter.chapterURL = link
                chapter.date = date
                chapter.chapterTitle = title
                list_of_chapters.append(chapter)
                print(number)
        logger.info('Found {} chapters.'.format(len(list_of_chapters)))
        return list_of_chapters

    def getListOfMangas(self):
        # http://www.onemanga2.com/manga-list/all/any/name-az/1/
        # http://www.onemanga2.com/manga-list/all/any/name-az/49/
        COUNT_PER_PAGE = 20
        searchURL = BASE_URL + '/manga-list/all/any/name-az/'
        list_of_all_manga_links = []
        self.list_of_all_mangas = []
        print('Finding mangas...')
        logger.info('Finding mangas...')
        for i in range(1, 50):
            # FIXME Check whether all pages have been read instead of assuming
            # that there are 49 pages!
            url = searchURL + str(i)
            logger.debug('Reading manga list from url "{}".'.format(url))
            result = PluginBase.loadURL(url)
            if result is None:
                return False
            parser = PluginBase.ParserBase(('div', 'class', 'det'), ('a', 'href'))
            parser.feed(result)
            if parser.targetCount > 1:
                for name, link in islice(zip(parser.targetData, parser.targetValues),
                                         COUNT_PER_PAGE):
                    m = Manga(name)
                    m.mangaURL = link
                    internalName = link.replace(BASE_URL, '').replace('/', '')
                    m.internalName = internalName
                    list_of_all_manga_links.append(link)
                    self.list_of_all_mangas.append(m)
            else:
                logger.warning('No mangas found on site.')
        print('Found {} mangas on site!'.format(len(self.list_of_all_mangas)))
        return self.list_of_all_mangas

    @memoized
    def __getInternalName(self, searchedManga):
        internalName = ''
        #internalName = name
        #internalName = str.lower(internalName)
        #internalName = str.replace(internalName, '-', '')
        #internalName = str.replace(internalName, ' ', '_')
        if not self.list_of_all_mangas:
            self.getListOfMangas()
        for manga in self.list_of_all_mangas:
            if manga.name == searchedManga.name:
                internalName = manga.internalName
                break
        return internalName


# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('No test implemented!')
