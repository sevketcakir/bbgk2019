from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QImage
import sys
import cv2
import time


class AnaEkran:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.win = uic.loadUi("anaekran.ui")
        self.win.action_ac.triggered.connect(self.ac)
        self.win.action_cik.triggered.connect(lambda : self.app.exit())
        self.win.action_sifrele.triggered.connect(self.sifrele)
        self.win.action_coz.triggered.connect(self.coz)
        self.win.action_farkli_kaydet.triggered.connect(self.farkli_kaydet)
        self.win.action_kameradan_yakala.triggered.connect(self.kameradan_yakala)
        self.win.show()
        self.image = None
        self.pixmap = None

    def ac(self):
        dosya_adi, ext = QtWidgets.QFileDialog.getOpenFileName(self.win, 'Resim dosyası aç', '.',
                                                               'Resim dosyaları(*.png *.jpg *.bmp)')
        if dosya_adi != '':
            self.image = cv2.imread(dosya_adi)
            self.resim_goster(self.win.resim, self.image)

    def resim_goster(self, bilesen, resim):
        yukseklik, genislik = resim.shape[:2]
        self.win.statusbar.showMessage(f"Resim boyutu: {genislik}x{yukseklik}")
        qformat = QtGui.QImage.Format_Indexed8
        if len(resim.shape) == 3:
            if resim.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        qimage = QImage(self.image.data,
                        resim.shape[1],
                        resim.shape[0],
                        resim.strides[0],  # <--- +++
                        qformat)
        qimage = qimage.rgbSwapped()

        self.pixmap = QtGui.QPixmap.fromImage(qimage)
        bilesen._pixmap = self.pixmap
        bilesen.setPixmap(self.pixmap.scaled(bilesen.width(), bilesen.height(), QtCore.Qt.KeepAspectRatio))

    def sifrele(self):
        if self.image is not None:
            anahtar, ok = QtWidgets.QInputDialog.getText(self.win, 'Şifreleme anahtarı', 'Şifreleme anahtarını girin:')

            if ok:
                anahtar = [ord(i) for i in anahtar]
                itr = 0
                for i in range(self.image.shape[0]):
                    for j in range(self.image.shape[1]):
                        for k in range(self.image.shape[2]):
                            self.image[i, j, k] = (self.image[i, j, k]+anahtar[itr]) % 256
                            itr = (itr + 1) % len(anahtar)
                self.resim_goster(self.win.resim, self.image)

    def coz(self):
        if self.image is not None:
            anahtar, ok = QtWidgets.QInputDialog.getText(self.win, 'Şifreleme anahtarı', 'Şifreleme anahtarını girin:')

            if ok:
                anahtar = [ord(i) for i in anahtar]
                itr = 0
                for i in range(self.image.shape[0]):
                    for j in range(self.image.shape[1]):
                        for k in range(self.image.shape[2]):
                            self.image[i, j, k] = (self.image[i, j, k]-anahtar[itr]) % 256
                            itr = (itr + 1) % len(anahtar)
                self.resim_goster(self.win.resim, self.image)

    def farkli_kaydet(self):
        dosya_adi, ext = QtWidgets.QFileDialog.getSaveFileName(self.win, 'Kaydedilecek resim dosyası', filter='Resim dosyaları(*.png *.jpg *.bmp)')
        if dosya_adi != '':
            if dosya_adi.endswith('.jpg'):
                cv2.imwrite(dosya_adi, self.image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            else:
                cv2.imwrite(dosya_adi, self.image)

    def kameradan_yakala(self):
        cap = cv2.VideoCapture(0)
        baslangic = time.time()
        while True:
            sure = time.time()-baslangic
            ret, self.image = cap.read()
            if sure >= 5:
                self.resim_goster(self.win.resim, self.image)
                break
            cv2.putText(self.image,str(5-int(sure)), (10,100), cv2.FONT_HERSHEY_TRIPLEX,4,
                        (255,255,255), 6, cv2.LINE_AA)
            self.resim_goster(self.win.resim, self.image)
            self.app.processEvents()



if __name__ == '__main__':
    anaekran = AnaEkran()
    sys.exit(anaekran.app.exec())