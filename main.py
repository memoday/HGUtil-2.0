import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import Qt
from datetime import datetime
import hwpMacro
import naverShorten
import checkNews as cn

__version__ = '0.0.1'

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
form = resource_path('ui/main.ui')

form_class = uic.loadUiType(form)[0]
print("프로그램이 구동됩니다.")

def crawlStart(urlList): 
    newsList = []

    for i in range(len(urlList)):
        title, press, content, publishedDate, publishedTime = cn.checkNews(urlList[i])
        shortenUrl = naverShorten.naverShorten(urlList[i])

        news = {
            'title' : title,
            'press' : press,
            'publishedDate' : publishedDate,
            'publishedTime' : publishedTime,
            'shortenUrl' : shortenUrl,
            'content': content,
            'summary' : 'summary',
            }
        newsList.append(news)

    return newsList

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #프로그램 기본설정
        # self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('HGUtil '+__version__)
        self.statusBar().showMessage('프로그램 정상 구동 중')

        self.btn_addNews.clicked.connect(self.addNews)
        self.btn_hwp.clicked.connect(self.exportHangul)
        self.btn_message.clicked.connect(self.exportMessage)
        self.input_link.returnPressed.connect(self.addNews)

        header = self.newsTable.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Stretch)

        self.btn_delete.clicked.connect(self.deleteRow)

    def addNews(self):
        self.newsTable.setSortingEnabled(False)
        try:
            input_link = []

            longUrl = self.input_link.text()
            longUrl = longUrl.replace(" ","")

            input_link.append(longUrl)
            if len(input_link) != 0:
                newsList = crawlStart(input_link)
                print(str(newsList))

                title = newsList[0]["title"]
                press = newsList[0]["press"]
                publishedDate = newsList[0]["publishedDate"]
                publishedTime = newsList[0]["publishedTime"]
                shortenUrl = newsList[0]["shortenUrl"]
                content = newsList[0]["content"]
                summary = newsList[0]["summary"]

                for i in range(len(input_link)):
                    row_index = self.newsTable.rowCount()
                    self.newsTable.insertRow(row_index)

                    self.combo = QComboBox() #신문/방송 or 인터넷 콤보박스 추가
                    self.combo.addItem("신문/방송")
                    self.combo.addItem("인터넷")
                    self.combo.setCurrentIndex(1)
                    self.checkbox = QCheckBox() #체크박스 추가

                    if publishedDate != "" and publishedTime != "":
                        date_obj = datetime.strptime(publishedDate, '%Y.%m.%d.')
                        time_obj = datetime.strptime(publishedTime,'%H:%M').time()
                        publishedDateTime = datetime.combine(date_obj.date(),time_obj)
                        publishedDateTime = publishedDateTime.strftime('%Y-%m-%dT%H:%M')
                    elif publishedDate != "" and publishedTime == "":
                        date_obj = datetime.strptime(publishedDate, '%Y.%m.%d.')
                        publishedDateTime = date_obj.strftime('%Y-m-%d')
                    elif publishedDate == "" and publishedTime != "":
                        time_obj = datetime.strptime(publishedTime,'%H:%M').time()
                        publishedDateTime = time_obj.strftime('T%H:%M')
                    else:
                        publishedDateTime = ""

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
        except Exception as e:
            self.statusBar().showMessage("addNews() 오류: "+str(e))
        self.newsTable.setSortingEnabled(True)

    def exportHangul(self):
        try:
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

                if publishedDateTime == "":
                    self.statusBar().showMessage('날짜가 입력되지 않은 기사가 있습니다.')
                    return
                publishedDate, publishedTime = publishedDateTime.split('T')
                publishedDate = publishedDate.replace("-",".")

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

            hwpMacro.main(paperNewsList,internetNewsList)
        except Exception as e:
            self.statusBar().showMessage("exportHangul 작업 실패: "+str(e))

    def exportMessage(self):
        try:
            rows = self.newsTable.rowCount()
            columns = self.newsTable.columnCount()
            print(rows)
            print(columns)

            totalNewsList = []
            checkedNewsList = []
            paperNewsList = []
            internetNewsList = []
            for i in range(rows):
                checked = self.newsTable.cellWidget(i,0).isChecked()
                newsType = self.newsTable.cellWidget(i,1).currentText() #table데이터를 배열화하는 작업
                press = self.newsTable.item(i,3).text()
                title = self.newsTable.item(i,4).text()
                summary = self.newsTable.item(i,6).text()
                shortenUrl = self.newsTable.item(i,7).text()
                # print(newsType)
                # print(publishedDateTime,press,title,content,summary,shortenUrl)

                news = {
                    'checked' : checked,
                    'title' : title,
                    'press' : press,
                    'shortenUrl' : shortenUrl,
                    'summary' : summary,
                    'newsType' : newsType,
                    }

                totalNewsList.append(news)
            
            for i in range(len(totalNewsList)): #체크된 기사들 checkedNewsList 배열로 이동
                if totalNewsList[i]['checked'] == True:
                    checkedNewsList.append(totalNewsList[i])
            
            for i in range(len(checkedNewsList)): #checkedNewsList에서 신문/방송 기사와 인터넷 기사 분류
                if checkedNewsList[i]["newsType"] == "신문/방송":
                    paperNewsList.append(checkedNewsList[i])
                elif checkedNewsList[i]["newsType"] == "인터넷":
                    internetNewsList.append(checkedNewsList[i])
            
            

        except Exception as e:
            self.statusBar().showMessage("exportMessage 작업 실패: "+str(e))

    def deleteRow(self):
        selected = self.newsTable.currentRow()
        self.newsTable.removeRow(selected)
        print(selected)

    def closeEvent(self, event):
        sys.exit(0)
        
    def exit(self) :
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()