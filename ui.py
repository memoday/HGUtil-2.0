import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import Qt
import main
from datetime import datetime
import hwpMacro

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


        table = self.newsTable #테이블 가로 길이 설정
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
        self.btn_hwp.clicked.connect(self.exportHangul)
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

                self.combo = QComboBox() #신문/방송 or 인터넷 콤보박스 추가
                self.combo.addItem("신문/방송")
                self.combo.addItem("인터넷")
                self.combo.setCurrentIndex(1)
                self.checkbox = QCheckBox() #체크박스 추가

                date_obj = datetime.strptime(publishedDate, '%Y.%m.%d.') #시간 순 정렬 편의를 위해 날짜/시간을 한 칸에 임시로 합쳐둠
                time_obj = datetime.strptime(publishedTime,'%H:%M').time()
                publishedDateTime = datetime.combine(date_obj.date(),time_obj)
                publishedDateTime = publishedDateTime.strftime('%Y-%m-%dT%H:%M')

                self.newsTable.setCellWidget(row_index,0,self.checkbox)
                self.newsTable.setCellWidget(row_index,1,self.combo)
                self.newsTable.setItem(row_index,2,QTableWidgetItem(publishedDateTime))
                self.newsTable.setItem(row_index,3,QTableWidgetItem(press))
                self.newsTable.setItem(row_index,4,QTableWidgetItem(title))
                self.newsTable.setItem(row_index,5,QTableWidgetItem(content))
                self.newsTable.setItem(row_index,6,QTableWidgetItem(summary))
                self.newsTable.setItem(row_index,7,QTableWidgetItem(shortenUrl))
            
            newsList.clear()
            input_link.clear()
        
        else:
            pass

    def exportHangul(self):
        rows = self.newsTable.rowCount()
        columns = self.newsTable.columnCount()
        print(rows)
        print(columns)

        finalNewsList = []
        paperNewsList = []
        internetNewsList = []
        for i in range(rows):
            newsType = self.newsTable.cellWidget(i,1).currentText() #table데이터를 배열화하는 작업
            publishedDateTime = self.newsTable.item(i,2).text()
            press = self.newsTable.item(i,3).text()
            title = self.newsTable.item(i,4).text()
            content = self.newsTable.item(i,5).text()
            summary = self.newsTable.item(i,6).text()
            shortenUrl = self.newsTable.item(i,7).text()
            # print(newsType)
            # print(publishedDateTime,press,title,content,summary,shortenUrl)

            publishedDate, publishedTime = publishedDateTime.split('T')

            news = {
                'title' : title,
                'press' : press,
                'publishedDate' : publishedDate,
                'publishedTime' : publishedTime,
                'shortenUrl' : shortenUrl,
                'content': content,
                'summary' : summary,
                'newsType' : newsType,
                }
            # print(publishedDateTime)
            # print(publishedDate)
            # print(publishedTime)

            finalNewsList.append(news)
        
        for i in range(len(finalNewsList)):
            if finalNewsList[i]["newsType"] == "신문/방송":
                paperNewsList.append(finalNewsList[i])
            elif finalNewsList[i]["newsType"] == "인터넷":
                internetNewsList.append(finalNewsList[i])

        print(paperNewsList)
        print('=========================')
        print(internetNewsList)
        hwpMacro.main(paperNewsList,internetNewsList)

            
    def newsOrganize(finalNewsList):
        print(finalNewsList)

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