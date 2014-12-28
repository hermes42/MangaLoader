#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import src.PluginBase as PluginBase
from src.PluginBase import find_re_in_site
from src.MangaBase import Manga
from src.MangaBase import Chapter

# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

logger = logging.getLogger('MangaLoader.MangaFoxPlugin')

BASE_URL = 'http://mangafox.me/'


# -------------------------------------------------------------------------------------------------
#  Plugin class
# -------------------------------------------------------------------------------------------------
class MangaFoxPlugin(PluginBase.PluginBase):

    def __init__(self):
        self.__domain = BASE_URL

    def getImage(self, image):
        global logger

        manga = image.chapter.manga
        chapter = image.chapter

        # http://mangafox.me/manga/coppelion/v19/c185/1.html
        url = '/'.join((self.__domain, self.__getInternalName(manga.name), str(chapter.chapterNo), str(image.imageNo)))
        result = PluginBase.loadURL(url)

        if result is None:
            return False

        logger.debug('start parsing')
        parser = PluginBase.ParserBase(('div', 'id', 'imgholder'), ('img', 'src'))
        parser.feed(result)

        logger.debug('targetCount = ' + str(parser.targetCount))
        if parser.targetCount < 1:
            logger.info('No image found in MangaReader site, maybe the chapter is not available.')
            return False

        if parser.targetCount > 1:
            logger.warning('{} images found in MangaReader site, maybe the chapter is not available.'.format(parser.targetCount))
            return False

        if parser.targetValue == '':
            logger.warning('No valid image url found in MangaReader site.')
            return False

        logger.debug('imageURL = {}'.format(parser.targetValue))
        image.imageUrl = parser.targetValue
        logger.debug('imageUrl found: {}'.format(parser.targetValue))
        return True

    def getListOfChapters(self, manga):
        """Gets list of all chapters currently available for a given manga.

        Regular expression was stolen from Bartosz Foder, licensed under BSD
        License (http://github.com/PImpek/MFD)!
        
        :param manga: describing the manga for which chapters should be found
                      including its name and the link of the main site
        :return: a list of chapters with all necessary information like their URLs
        """
        url = manga.manga_url
        logger.info('Looking for chapters of manga "{}" ({}).'.format(manga.name, manga.manga_url))
        logger.info('Finding chapters...')
        regex = r"<a href=\"((?:https?://)?(?:[\da-z\.\-/\_]+))\"\s+title=\"(?:[A-Za-z0-9\s\\/\-\_!@,\.\*\+]+)\"\s+class=\"tips\">([A-Za-z0-9\s\\/\-\_!@,\.\*\+]+)\s*</a>"
        link_list = find_re_in_site(url, regex)
        logger.info('Found {} chapters.'.format(len(link_list)))
        list_of_chapters = list()
        for link, name in link_list:
            import re
            number = int(re.findall('\d+$', name)[0])
            chapter = Chapter(manga.name, number)
            list_of_chapters.append(chapter)
        return list_of_chapters

    def getListOfMangas(self):
        url = '/'.join((self.__domain, 'manga'))
        result = PluginBase.loadURL(url)
        if result is None:
            return False
        print('Finding mangas...')
        logger.debug('Finding mangas...')
        parser = PluginBase.ParserBase(('div', 'class', 'manga_list'), ('a', 'href'))
        parser.feed(result)
        print('Found {} mangas on site!'.format(parser.targetCount))
        if parser.targetCount > 1:
            list_of_all_mangas = list()
            for name, link in zip(parser.targetData, parser.targetValues):
                m = Manga(name)
                m.manga_url = link
                list_of_all_mangas.append(m)
            # remove first element because this is not actually a manga :-)
            del list_of_all_mangas[0]
        else:
            logger.warning('No mangas found on site.')
        return list_of_all_mangas

    def __getInternalName(self, name):
        internalName = name
        internalName = str.lower(internalName)
        internalName = str.replace(internalName, ' ', '-')
        return internalName


# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('no test implemented')
