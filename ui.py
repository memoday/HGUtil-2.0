import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import Qt

__version__ = '0.0.1'

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
form = resource_path('ui/main.ui')

form_class = uic.loadUiType(form)[0]
print("프로그램이 구동됩니다.")

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #프로그램 기본설정
        # self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('HGUtil '+__version__)
        self.statusBar().showMessage('프로그램 정상 구동 중')
        self.btn_delete.clicked.connect(self.deleteRow)


        self.combo = QComboBox()
        self.combo.addItem("신문/방송")
        self.combo.addItem("인터넷")
        self.combo.setCurrentIndex(1)
        self.paperTable.setCellWidget(0,0,self.combo)

    def addRow(self):
        selected = self.paperTable.currentRow()
        self.paperTable.insertRow(selected+1)
        self.paperTable.selectRow(selected + 1)

    def deleteRow(self):
        selected = self.paperTable.currentRow()
        self.paperTable.removeRow(selected)

    def closeEvent(self, event):
        sys.exit(0)

    def exit(self) :
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()