from PyQt5.QtWidgets import *
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
layout.addWidget(QLineEdit('Merhaba'))
window.setLayout(layout)
window.show()
app.exec_()