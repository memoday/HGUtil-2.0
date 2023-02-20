import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import Qt
import main

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


        table = self.newsTable

        table.setColumnWidth(0, 5)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 70)
        table.setColumnWidth(4, 200)
        table.setColumnWidth(5, 100)
        table.setColumnWidth(6, 100)
        table.setColumnWidth(7, 100)
        table.setColumnWidth(8, 50)

        self.btn_addNews.clicked.connect(self.addNews)
        self.input_link.setText("https://n.news.naver.com/mnews/article/001/0013766266?sid=102")


        #첫 번째 주소에 예시값 삽입
        self.btn_delete.clicked.connect(self.deleteRow)

    def addNews(self):
        input_link = []

        input_link.append(self.input_link.text())
        if len(input_link) != 0:
            newsList = main.crawl(input_link)
            print(str(newsList))

            title = newsList[0]["title"]
            press = newsList[0]["press"]
            publishedDate = newsList[0]["publishedDate"]
            publishedTime = newsList[0]["publishedTime"]
            shortenUrl = newsList[0]["shortenUrl"]
            content = newsList[0]["content"]
            summary = newsList[0]["summary"]

            print(title,press,publishedDate,publishedTime,shortenUrl,content,summary)

            for i in range(len(input_link)):
                row_index = self.newsTable.rowCount()
                self.newsTable.insertRow(row_index)
                self.newsTable.selectRow(row_index)

                self.combo = QComboBox() #추후에 콤보박스 기준으로 데이터 분류 예정
                self.combo.addItem("신문/방송")
                self.combo.addItem("인터넷")
                self.combo.setCurrentIndex(1)

                self.checkbox = QCheckBox()

                self.newsTable.setCellWidget(row_index,0,self.checkbox)

                self.newsTable.setCellWidget(row_index,1,self.combo)
                self.newsTable.setItem(row_index,2,QTableWidgetItem(publishedDate))
                self.newsTable.setItem(row_index,3,QTableWidgetItem(press))
                self.newsTable.setItem(row_index,4,QTableWidgetItem(title))
                self.newsTable.setItem(row_index,5,QTableWidgetItem(content))
                self.newsTable.setItem(row_index,6,QTableWidgetItem(summary))
                self.newsTable.setItem(row_index,7,QTableWidgetItem(shortenUrl))
            
            newsList.clear()
            input_link.clear()
        
        else:
            pass



    def addRow(self):
        selected = self.newsTable.currentRow()
        self.newsTable.insertRow(selected+1)
        self.newsTable.selectRow(selected + 1)

    def deleteRow(self):
        selected = self.newsTable.currentRow()
        self.newsTable.removeRow(selected)

    def closeEvent(self, event):
        sys.exit(0)

    def exit(self) :
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()