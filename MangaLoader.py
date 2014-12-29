#!/usr/bin/python3

import os
import sys
import time
import logging
import logging.handlers
from optparse import OptionParser

from src import MangaBase
from src.plugins import MangaReaderPlugin
from src.plugins import MangaFoxPlugin
from src.plugins import MangaHerePlugin
from src.plugins import EatMangaPlugin


APP_NAME = 'MangaLoader'
APP_VERSION = 'v0.1'


# -------------------------------------------------------------------------------------------------
#  logging
# -------------------------------------------------------------------------------------------------

def create_logger():
    """Creates logger for this application."""
    LOG_FORMAT = '%(asctime)-23s [%(levelname)8s] %(name)-15s %(message)s (%(filename)s:%(lineno)s)'
    LOG_LEVEL = logging.DEBUG
    LOG_FILENAME = os.path.join(os.getenv('HOME'), '.MangaLoader', 'mangaloader.log')
    logger = logging.getLogger('MangaLoader')
    logger.setLevel(LOG_LEVEL)
    # add logging to screen
    log_to_screen = logging.StreamHandler(sys.stdout)
    log_to_screen.setLevel(logging.WARNING)
    logger.addHandler(log_to_screen)
    # add logging to file
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                       maxBytes=262144,
                                                       backupCount=5)
    log_to_file.setLevel(LOG_LEVEL)
    log_to_file.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(log_to_file)
    return logger


# -------------------------------------------------------------------------------------------------
#  <module>
# -------------------------------------------------------------------------------------------------

# test with:
#  python MangaLoader.py --MangaReader -n Claymore -r 14 20 -o /home/markus/Desktop/New Mangas


def parse_and_load():

    #####
    # Specify options and parse arguments.
    #####

    logger.info('MangaLoader started')

    logger.debug('starting to parse options and args')

    usage = 'usage: %prog [options]'
    parser = OptionParser(usage)
    parser.add_option('--version',
                    action='store_true',
                    dest='version',
                    help='show version information')
    parser.add_option('--MangaReader',
                    action='store_true',
                    dest='MangaReader',
                    help='use MangaReader plugin')
    parser.add_option('--MangaFox',
                    action='store_true',
                    dest='MangaFox',
                    help='use MangaFox plugin')
    parser.add_option('--MangaHere',
                    action='store_true',
                    dest='MangaHere',
                    help='use MangaHere plugin')
    parser.add_option('--EatManga',
                    action='store_true',
                    dest='EatManga',
                    help='use EatManga plugin')
    parser.add_option('-z',
                    action='store_true',
                    dest='Zip',
                    help='create cbz files')
    parser.add_option('-n',
                    action='store',
                    type='string',
                    dest='name',
                    metavar='NAME',
                    help='name of the manga')
    parser.add_option('-r',
                    action='store',
                    type='int',
                    dest='range',
                    nargs=2,
                    metavar='FROM TO',
                    help='load a range of chapters')
    parser.add_option('-i',
                    action='store',
                    type='int',
                    dest='image',
                    nargs=2,
                    metavar='CHAPTER IMAGE',
                    help='load a single image (chapterNo, imageNo)')
    parser.add_option('-o',
                    action='store',
                    type='string',
                    dest='output',
                    metavar='DEST_DIR',
                    help='destination directory')

    (options, args) = parser.parse_args()

    if options.version != None:
        print('{} {}'.format(APP_NAME, APP_VERSION))
        sys.exit()

    if options.name is None:
        logger.error('Missing manga name.')
        sys.exit()

    if options.output is None:
        logger.error('Missing destination folder.')
        sys.exit()

    if (options.range is None) and (options.image is None):
        logger.error('Specify at least range of images.')
        sys.exit()

    pluginCount = 0
    if (options.MangaReader is not None):
        pluginCount = pluginCount + 1
    if (options.MangaFox is not None):
        pluginCount = pluginCount + 1
    if (options.MangaHere is not None):
        pluginCount = pluginCount + 1
    if (options.EatManga is not None):
        pluginCount = pluginCount + 1

    if  pluginCount <= 0:
        logger.warn('No plugin specified, using MangaFox.')
        options.MangaFox = True
    if  pluginCount > 1:
        logger.error('Specify exactly one plugin.')
        sys.exit()

    logger.debug('options parse done')


    #####
    # Start actual manga load with specified parameter & arguments.
    #####

    start_time = time.time()
    logger.debug('start time: %.2f s' %(start_time))

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

    logger.info('loading plugin')
    if options.MangaReader is not None:
        plugin = MangaReaderPlugin.MangaReaderPlugin()
        logger.debug('using MangaLoader plugin')
    elif options.MangaFox is not None:
        plugin = MangaFoxPlugin.MangaFoxPlugin()
        logger.debug('using MangaFox plugin')
    elif options.MangaHere is not None:
        plugin = MangaHerePlugin.MangaHerePlugin()
        logger.debug('using MangaHere plugin')
    elif options.EatManga is not None:
        plugin = EatMangaPlugin.EatMangaPlugin()
        logger.debug('using EatManga plugin')

    logger.info('loading Loader')
    loader = MangaBase.Loader(plugin, destDir)

    if useRange:
        logger.info('loading chapters ' + str(startChapter) + ' - ' + str(endChapter))
        for i in range(startChapter, endChapter+1):
            loader.handleChapter(mangaName, i)
            if doZip:
                loader.zipChapter(mangaName, i)

    else:
        logger.info('loading image ' + str(chapter) + ' / ' + str(image))
        loader.handleImage(mangaName, chapter, image)
        if doZip:
                loader.zipChapter(mangaName, chapter)

    end_time = time.time()
    logger.debug('end time: %.2f s' %(end_time))
    logger.info('elapsed time: %.2f s' %(end_time - start_time))
    print(('Elapsed Time: %.2f s' %(end_time - start_time)))

    logger.info('MangaLoader done')


if __name__ == '__main__':
    global logger
    logger = create_logger()
    logger.info('Starting {}...'.format(APP_NAME))
    
    parse_and_load()
    
    #from src.plugins import MangaFoxPlugin
    #from src.MangaBase import Image
    #m = MangaFoxPlugin.MangaFoxPlugin()
    #x = m.getListOfMangas()
    #for i in x:
    #    if i.name == 'Coppelion':
    #        c = m.getListOfChapters(i)
    #n = MangaBase.Manga('Coppelion')
    #n.manga_url = 'http://mangafox.me/manga/coppelion/'
    #c = m.getListOfChapters(n)
    #i = Image(c[14], 4)
    #m.getImage(i)
