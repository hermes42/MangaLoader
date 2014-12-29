#!/usr/bin/python3

import os
import sys
#import time
import logging
import logging.handlers

from PyQt4 import QtGui
from PyQt4 import QtCore

#from src import MangaBase
from gui import viewer
from gui import loader
#from src.plugins import MangaFoxPlugin


APP_NAME = 'MangaLoaderGUI'
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

def startGUI():
    logger.info('MangaLoaderGUI started.')
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    #app.aboutToQuit.connect(handle_exit)
    main = QtGui.QMainWindow()
    main.setWindowTitle('MangaLoader')
    #main.setWindowState(QtCore.Qt.WindowMaximized)
    #v = viewer.ImageView(main)
    v = loader.LoaderWindow(main)
    main.setCentralWidget(v)
    main.show()
    sys.exit(app.exec_())

    #logger.info('loading Loader')
    #plugin = MangaFoxPlugin.MangaFoxPlugin()    
    #loader = MangaBase.Loader(plugin, destDir)
    #if useRange:
    #    logger.info('loading chapters ' + str(startChapter) + ' - ' + str(endChapter))
    #    for i in range(startChapter, endChapter+1):
    #        loader.handleChapter(mangaName, i)
    #        if doZip:
    #            loader.zipChapter(mangaName, i)
    #else:
    #    logger.info('loading image ' + str(chapter) + ' / ' + str(image))
    #    loader.handleImage(mangaName, chapter, image)
    #    if doZip:
    #            loader.zipChapter(mangaName, chapter)
    #end_time = time.time()
    #logger.debug('end time: %.2f s' %(end_time))
    #logger.info('elapsed time: %.2f s' %(end_time - start_time))
    #print(('Elapsed Time: %.2f s' %(end_time - start_time)))
    
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
    logger.info('MangaLoader done')


if __name__ == '__main__':
    global logger
    logger = create_logger()
    logger.info('Starting {}...'.format(APP_NAME))
    startGUI()
