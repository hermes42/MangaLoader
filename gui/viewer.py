
"""
Image widgets for showing manga pages on fullscreen or at least scaled to
maximum size.

Created on Mon Dec 29 12:42:49 2014

@author: Christian Wichmann
"""


import logging
from PyQt4 import QtGui
from PyQt4 import QtCore


logger = logging.getLogger('MangaLoader.gui')


class ImageView(QtGui.QWidget):
    """Shows a widget containing an image."""
    def __init__(self, parent):
        super(ImageView, self).__init__(parent)
        self.main_gui = parent
        self.create_fonts()
        self.setup_ui()
        self.set_signals_and_slots()

    def resizeEvent(self, event):
        super(ImageView, self).resizeEvent(event)
        # handle resizing of image
        new_size = event.size()
        new_size.setWidth(new_size.width() - 125)
        new_size.setHeight(new_size.height() - 10)
        self.scaled_image = self.image.scaled(new_size, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.scaled_image)

    def create_fonts(self):
        self.label_font = QtGui.QFont()
        self.label_font.setPointSize(22)

    def setup_ui(self):
        # add previous button
        grid = QtGui.QGridLayout()
        previous_button = QtGui.QPushButton('Previous')
        grid.addWidget(previous_button, 0, 0, QtCore.Qt.AlignCenter)
        # add image label
        self.image_label = QtGui.QLabel()
        self.image = QtGui.QPixmap('./Coppelion/Coppelion 14/12.jpg')        
        self.scaled_image = self.image.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.scaled_image)
        self.image_label.setScaledContents(True)
        grid.addWidget(self.image_label, 0, 1, QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        # add next button
        next_button = QtGui.QPushButton('Next')
        grid.addWidget(next_button, 0, 2, QtCore.Qt.AlignCenter)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 100)
        grid.setColumnStretch(2, 0)
        self.setLayout(grid)

    def set_signals_and_slots(self):
        """Sets all signals and slots for this widget."""
        pass

    #@QtCore.pyqtSlot(int)
    #def on_resize(self):
    #    print('resize')
