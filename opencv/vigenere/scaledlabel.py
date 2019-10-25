from PyQt5 import QtCore,QtWidgets, QtGui


class ScaledLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self)
        self._pixmap = QtGui.QPixmap(self.pixmap())

    def resizeEvent(self, event):
        if self._pixmap is not None:
            self.setPixmap(self._pixmap.scaled(
                self.width(), self.height(),
                QtCore.Qt.KeepAspectRatio))