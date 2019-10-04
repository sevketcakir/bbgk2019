from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

def tiklama():
    form.lineEdit.setText(form.lineEdit.text()+' merhaba')


Form, Window = uic.loadUiType("uber.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

form.pushButton.clicked.connect(tiklama)

window.show()
app.exec_()