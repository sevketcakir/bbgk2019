import cv2
import numpy as np
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QImage
import sys


def resim_goster(bilesen, resim):
    yukseklik, genislik = resim.shape[:2]
    win.statusbar.showMessage(f"Resim boyutu: {genislik}x{yukseklik}")
    qformat = QtGui.QImage.Format_Indexed8
    if len(resim.shape) == 3:
        if resim.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888
    qimage = QImage(resim.data,
                    resim.shape[1],
                    resim.shape[0],
                    resim.strides[0],  # <--- +++
                    qformat)
    qimage = qimage.rgbSwapped()

    pixmap = QtGui.QPixmap.fromImage(qimage)
    bilesen._pixmap = pixmap
    bilesen.setPixmap(pixmap.scaled(bilesen.width(), bilesen.height(), QtCore.Qt.KeepAspectRatio))

def cizgifilm(img):
    gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gri = cv2.medianBlur(gri, 7)
    kenarlar = cv2.Laplacian(gri, cv2.CV_8U, ksize=5)
    ret, maske = cv2.threshold(kenarlar, 100, 255, cv2.THRESH_BINARY_INV)

    for i in range(10):
        img = cv2.bilateralFilter(img, 5, 5, 7)
    dst = np.zeros(gri.shape)
    dst = cv2.bitwise_and(img, img, mask=maske)
    return dst

def vintage(img):
    rows, cols = img.shape[:2]
    # Create a Gaussian filter
    kernel_x = cv2.getGaussianKernel(cols, 200)
    kernel_y = cv2.getGaussianKernel(rows, 200)
    kernel = kernel_y * kernel_x.T
    filter = 255 * kernel / np.linalg.norm(kernel)
    vintage_im = np.copy(img)
    # for each channel in the input image, we will apply the above filter
    for i in range(3):
        vintage_im[:, :, i] = vintage_im[:, :, i] * filter

    return vintage_im

def baslat():
    while True:
        ret, frame = cap.read()
        if win.comboBox.currentText()=="Gri seviye":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif win.comboBox.currentText()=="Gaussian Blur":
            try:
                frame = cv2.GaussianBlur(frame, (11,11),cv2.BORDER_DEFAULT)
            except Exception as hata:
                print(str(hata))
        elif win.comboBox.currentText()=="Çizgi Film":
            try:
                frame = cizgifilm(frame)
            except Exception as hata:
                print(str(hata))
        elif win.comboBox.currentText()=="Vintage":
            frame = vintage(frame)
        elif win.comboBox.currentText()=="Canny":
            frame = cv2.Canny(frame,80,300)
        resim_goster(win.label, frame)
        app.processEvents()

cap = cv2.VideoCapture(0)
app = QtWidgets.QApplication([])
win = uic.loadUi('goruntu.ui')
win.baslat.clicked.connect(baslat)

model=QStringListModel(["İşlem yok","Gri seviye","Gaussian Blur","Çizgi Film","Vintage", "Canny"])
win.comboBox.setModel(model)


win.show()

#cap.release()
sys.exit(app.exec())

