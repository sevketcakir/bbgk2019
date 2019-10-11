from os.path import expanduser
from PyQt5.QtWidgets import *

home_directory = expanduser('~')

app = QApplication([])
model = QDirModel()
view = QTreeView()
view.setModel(model)
view.setRootIndex(model.index(home_directory))

def tiklama(qmi):
    print(str(qmi.data()))

view.clicked.connect(tiklama)

view.show()
app.exec_()