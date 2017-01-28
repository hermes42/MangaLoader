#!/usr/bin/python3

import os
import sys
import logging
import logging.handlers

from PyQt4 import QtGui

from gui import loader


APP_NAME = 'MangaLoaderGUI'
APP_VERSION = 'v0.2'


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
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=262144, backupCount=5)
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
    main = QtGui.QMainWindow()
    main.setWindowTitle('MangaLoader')
    # create main window and show it
    v = loader.LoaderWindow(main)
    main.setCentralWidget(v)
    main.show()
    sys.exit(app.exec_())
    logger.info('MangaLoader done.')


if __name__ == '__main__':
    global logger
    logger = create_logger()
    logger.info('Starting {}...'.format(APP_NAME))
    startGUI()
