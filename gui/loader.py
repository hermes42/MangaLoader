
"""
Graphical user interface to load manga from various sites.

Created on Mon Dec 29 13:44:49 2014

@author: Christian Wichmann
"""


import logging
import os
import pickle
from PyQt4 import QtGui
from PyQt4 import QtCore

from src.plugins import MangaFoxPlugin
from src import MangaBase


logger = logging.getLogger('MangaLoader.gui')


MANGA_LIST_FILE = 'manga_list.data'


class LoaderWindow(QtGui.QWidget):
    """Shows a GUI to download mangas."""
    def __init__(self, parent):
        super(LoaderWindow, self).__init__(parent)
        self.main_gui = parent
        self.manga_store_path = os.getcwd()
        self.plugin = MangaFoxPlugin.MangaFoxPlugin()
        self.manga_list = []
        self.chapter_count = 1
        self.create_fonts()
        self.setup_ui()
        self.set_signals_and_slots()

    def create_fonts(self):
        self.label_font = QtGui.QFont()
        self.label_font.setPointSize(22)

    def setup_ui(self):
        # setup grid layout
        grid = QtGui.QGridLayout()
        grid.setSpacing(15)
        # add manga chooser
        grid.addWidget(QtGui.QLabel('Load manga: '), 0, 0)
        grid.addWidget(self.buildMangaComboBox(), 0, 1, 1, 2)
        self.update_list_button = QtGui.QPushButton('Update...')
        grid.addWidget(self.update_list_button, 0, 3)
        # add chapter chooser
        grid.addWidget(QtGui.QLabel('From chapter: '), 1, 0)
        self.chapter_begin = QtGui.QSpinBox()
        self.chapter_begin.setValue(1)
        self.chapter_begin.setMinimum(1)
        self.chapter_begin.setMaximum(1000)
        self.chapter_begin.setSingleStep(1)
        grid.addWidget(self.chapter_begin, 1, 1)
        grid.addWidget(QtGui.QLabel('until chapter: '), 1, 2)
        self.chapter_end = QtGui.QSpinBox()
        self.chapter_end.setValue(10)
        self.chapter_end.setMinimum(1)
        self.chapter_end.setMaximum(1000)
        self.chapter_end.setSingleStep(1)
        grid.addWidget(self.chapter_end, 1, 3)
        # add directory chooser
        grid.addWidget(QtGui.QLabel('Into directory: '), 2, 0)
        self.directory_button = QtGui.QPushButton(self.manga_store_path)
        grid.addWidget(self.directory_button, 2, 1, 1, 3)
        # add progressbar
        self.loader_progress = QtGui.QProgressBar()
        grid.addWidget(self.loader_progress, 3, 0, 1, 4)
        # add load button
        self.load_button = QtGui.QPushButton('Load...')
        grid.addWidget(self.load_button, 5, 0, QtCore.Qt.AlignLeft)
        # add quit button
        self.quit_button = QtGui.QPushButton('Quit')
        grid.addWidget(self.quit_button, 5, 3, QtCore.Qt.AlignRight)
        # setup grid layout
        #grid.setColumnStretch(0, 1)
        #grid.setColumnStretch(1, 1)
        #grid.setColumnStretch(2, 1)
        #grid.setColumnStretch(3, 1)
        self.setLayout(grid)

    def buildMangaComboBox(self):
        self.mangaComboBox = QtGui.QComboBox()
        self.load_manga_list_from_file()
        return self.mangaComboBox

    def set_signals_and_slots(self):
        """Sets all signals and slots for this widget."""
        self.quit_button.clicked.connect(self.main_gui.close)
        self.directory_button.clicked.connect(self.on_choose_directory)
        self.load_button.clicked.connect(self.on_load_manga)
        self.mangaComboBox.currentIndexChanged.connect(self.on_update_chapter_fields)
        self.update_list_button.clicked.connect(self.on_update_manga_list)

    def load_manga_list_from_file(self):
        try:
            with open(MANGA_LIST_FILE, 'rb') as f:
                self.manga_list = pickle.load(f)
                for manga in self.manga_list:
                    self.mangaComboBox.addItem(manga.name)
        except FileNotFoundError:
            logger.warn('No manga list file found.')
            self.on_update_manga_list()

    @QtCore.pyqtSlot()
    def on_update_manga_list(self):
        # TODO Load mangas in background and update combo box regularly?!
        # load comboBox with items
        self.manga_list = self.plugin.getListOfMangas()
        for manga in self.manga_list:
            self.mangaComboBox.addItem(manga.name)
        # store manga list in file
        with open(MANGA_LIST_FILE, 'wb') as f:
            # pickle the manga list using the highest protocol available
            pickle.dump(self.manga_list, f, pickle.HIGHEST_PROTOCOL)

    @QtCore.pyqtSlot()
    def on_choose_directory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select directory to save mangas...')
        self.manga_store_path = directory
        self.directory_button.setText(self.manga_store_path)
        logger.debug('Choosen directory: "{}".'.format(directory))

    @QtCore.pyqtSlot()
    def on_load_manga(self):
        logger.info('Loading Loader...')
        loader = MangaBase.Loader(self.plugin, self.manga_store_path)
        startChapter = self.chapter_begin.value()
        endChapter = self.chapter_end.value()
        self.chapter_count = endChapter - startChapter
        logger.info('Loading chapters {} - {}'.format(str(startChapter), str(endChapter)))
        self.loader_progress.setRange(startChapter - 1, endChapter)
        self.loader_progress.setValue(startChapter - 1)
        # enforce event processing
        QtGui.QApplication.processEvents()
        for i in range(startChapter, endChapter + 1):
            loader.handleChapter(self.mangaComboBox.currentText(), i)
            self.loader_progress.setValue(i)
            # enforce event processing
            QtGui.QApplication.processEvents()
            #if doZip:
            #    loader.zipChapter(mangaName, i)

    @QtCore.pyqtSlot()
    def on_update_chapter_fields(self):
        chosen_manga = self.mangaComboBox.currentText()
        logger.debug('Combo box changed to {}.'.format(chosen_manga))
        # look for chosen manga and get chapter list
        for manga in self.manga_list:
            if manga.name == chosen_manga:
                chosen_manga = manga
                break
        chapter_list = self.plugin.getListOfChapters(chosen_manga)
        # set max and min for input fields
        chapter_number_list = [x.chapterNo for x in chapter_list]
        if chapter_number_list:
            maximum = max(chapter_number_list)
            minimum = min(chapter_number_list)
            self.chapter_begin.setMinimum(minimum)
            self.chapter_begin.setMaximum(maximum)
            self.chapter_end.setMinimum(minimum)
            self.chapter_end.setMaximum(maximum)
