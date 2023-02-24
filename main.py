import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import *
from datetime import datetime
import hwpMacro
import naverShorten
import checkNews as cn
import toMessage
from PyQt5.QtCore import *

__version__ = 'v1.0.0'

settings = QSettings("table.ini", QSettings.IniFormat)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
icon = resource_path('assets/icon.ico')
form = resource_path('ui/main.ui')
form_message = resource_path('ui/message.ui')

form_class = uic.loadUiType(form)[0]
form_messageWindow = uic.loadUiType(form_message)[0]
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
            'summary' : '',
            }
        newsList.append(news)

    return newsList

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #프로그램 기본설정
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('HGUtil '+__version__)
        self.statusBar().showMessage('프로그램 정상 구동 중')

        self.btn_addNews.clicked.connect(self.addNews)
        self.btn_hwp.clicked.connect(self.exportHangul)
        self.btn_message.clicked.connect(self.exportMessage)
        self.input_link.returnPressed.connect(self.addNews)
        self.btn_exit.clicked.connect(self.exit)
        self.btn_save.clicked.connect(self.save)
        self.btn_load.clicked.connect(self.load)

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

            self.messageWindow = messageWindow(paperNewsList,internetNewsList)
            self.messageWindow.exec()
            self.show()
            

        except Exception as e:
            self.statusBar().showMessage("exportMessage 작업 실패: "+str(e))

    def deleteRow(self):
        selected = self.newsTable.currentRow()
        self.newsTable.removeRow(selected)
        print(selected)

    def save(self):
        rowCount = self.newsTable.rowCount()
        if rowCount == 0:
            self.statusBar().showMessage('테이블에 저장할 데이터가 존재하지 않습니다.')
        tableList = []
        for i in range(rowCount):
            checked = self.newsTable.cellWidget(i,0).isChecked()
            newsType = self.newsTable.cellWidget(i,1).currentText() #table데이터를 배열화하는 작업
            publishedDateTime = self.newsTable.item(i,2).text()
            press = self.newsTable.item(i,3).text()
            title = self.newsTable.item(i,4).text()
            content = self.newsTable.item(i,5).text()
            summary = self.newsTable.item(i,6).text()
            shortenUrl = self.newsTable.item(i,7).text()

            news = {
                'checked' : checked,
                'title' : title,
                'publishedDateTime' : publishedDateTime,
                'press' : press,
                'shortenUrl' : shortenUrl,
                'content' : content,
                'summary' : summary,
                'newsType' : newsType,
                'shortenUrl' : shortenUrl,
                }   

            tableList.append(news)
        settings.setValue("Table", tableList)
        print('QSettings Saved')
        self.statusBar().showMessage('테이블이 table.ini에 저장되었습니다.')
    
    def load(self):
        try: 
            ini = settings.value("Table")

            self.newsTable.setRowCount(len(ini))

            self.checkbox = QCheckBox() #체크박스 추가

            for i in range(len(ini)):
                checked = ini[i]['checked']
                newsType = ini[i]['newsType']
                publishedDateTime = ini[i]['publishedDateTime']
                press = ini[i]['press']
                title = ini[i]['title']
                content = ini[i]['content']
                summary = ini[i]['summary']
                shortenUrl = ini[i]['shortenUrl']
                
                checked = str(checked)

                if checked == 'False':
                    self.newsTable.setCellWidget(i,0,QCheckBox())
                else:
                    checkedBox = QCheckBox()
                    self.newsTable.setCellWidget(i,0,checkedBox)
                    checkedBox.toggle()
                
                self.combo = QComboBox() #신문/방송 or 인터넷 콤보박스 추가
                self.combo.addItem("신문/방송")
                self.combo.addItem("인터넷")

                if newsType == "신문/방송":
                    self.combo.setCurrentIndex(0)
                else:
                    self.combo.setCurrentIndex(1)

                self.newsTable.setCellWidget(i,1,self.combo)
                self.newsTable.setItem(i,2,QTableWidgetItem(publishedDateTime))
                self.newsTable.setItem(i,3,QTableWidgetItem(press))
                self.newsTable.setItem(i,4,QTableWidgetItem(title))
                self.newsTable.setItem(i,5,QTableWidgetItem(content))
                self.newsTable.setItem(i,6,QTableWidgetItem(summary))
                self.newsTable.setItem(i,7,QTableWidgetItem(shortenUrl))
        except Exception as e:
            self.statusBar().showMessage('load() Error: '+str(e))

    def closeEvent(self, event):
        sys.exit(0)
        
    def exit(self) :
        sys.exit(0)

class messageWindow(QDialog,form_messageWindow):
    
    def __init__(self,paperNewsList,internetNewsList):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(icon))

        self.show()

        header = self.paperNewsTable.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        header = self.internetNewsTable.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        global pNewsList
        global iNewsList

        pNewsList = paperNewsList
        iNewsList = internetNewsList

        self.btn_internetUp.clicked.connect(self.internetUp)
        self.btn_internetDown.clicked.connect(self.internetDown)
        self.btn_paperUp.clicked.connect(self.paperUp)
        self.btn_paperDown.clicked.connect(self.paperDown)
        self.btn_run.clicked.connect(self.toMessage)
        self.btn_exit.clicked.connect(self.exit)

        SP_TitleBarShadeButton = self.style().standardIcon(QStyle.SP_TitleBarShadeButton)
        SP_TitleBarUnshadeButton = self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton)

        self.btn_internetUp.setIcon(SP_TitleBarShadeButton)
        self.btn_internetDown.setIcon(SP_TitleBarUnshadeButton)
        self.btn_paperUp.setIcon(SP_TitleBarShadeButton)
        self.btn_paperDown.setIcon(SP_TitleBarUnshadeButton)

        self.paperNewsTable.setRowCount(len(pNewsList)) #전달받은 데이터 테이블화 작업
        self.internetNewsTable.setRowCount(len(iNewsList))

        for i in range(len(pNewsList)):
            self.paperNewsTable.setItem(i,0,QTableWidgetItem(pNewsList[i]['press']))
            self.paperNewsTable.setItem(i,1,QTableWidgetItem(pNewsList[i]['title']))

        for i in range(len(iNewsList)):
            self.internetNewsTable.setItem(i,0,QTableWidgetItem(iNewsList[i]['press']))
            self.internetNewsTable.setItem(i,1,QTableWidgetItem(iNewsList[i]['title']))

        self.toMessage()

    def internetUp(self):
        global pNewsList
        global iNewsList
        selectedRow = self.internetNewsTable.currentRow()
        if selectedRow == 0:
            print('stopped')
        else:
            try:
                print('moved')
                newsDataSwapList = []

                press = self.internetNewsTable.item(selectedRow,0).text()
                title = self.internetNewsTable.item(selectedRow,1).text()
                newsData = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData)

                press = self.internetNewsTable.item(selectedRow-1,0).text()
                title = self.internetNewsTable.item(selectedRow-1,1).text()
                newsData2 = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData2)

                self.internetNewsTable.setItem(selectedRow-1,0,QTableWidgetItem(newsDataSwapList[0]['press']))
                self.internetNewsTable.setItem(selectedRow-1,1,QTableWidgetItem(newsDataSwapList[0]['title']))
                self.internetNewsTable.setItem(selectedRow,0,QTableWidgetItem(newsDataSwapList[1]['press']))
                self.internetNewsTable.setItem(selectedRow,1,QTableWidgetItem(newsDataSwapList[1]['title']))

                iTemp = iNewsList[selectedRow]
                iNewsList[selectedRow] = iNewsList[selectedRow-1]
                iNewsList[selectedRow-1] = iTemp

                self.internetNewsTable.selectRow(selectedRow-1)

                self.toMessage()
            except Exception as e:
                print('Error: '+str(e))

    def internetDown(self):
        global pNewsList
        global iNewsList
        selectedRow = self.internetNewsTable.currentRow()
        rowCount = self.internetNewsTable.rowCount()
        if selectedRow == -1 or selectedRow+1 == rowCount:
            print('stopped')
        else:
            try:
                print('moved')
                newsDataSwapList = []

                press = self.internetNewsTable.item(selectedRow,0).text()
                title = self.internetNewsTable.item(selectedRow,1).text()
                newsData = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData)

                press = self.internetNewsTable.item(selectedRow+1,0).text()
                title = self.internetNewsTable.item(selectedRow+1,1).text()
                newsData2 = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData2)

                self.internetNewsTable.setItem(selectedRow+1,0,QTableWidgetItem(newsDataSwapList[0]['press']))
                self.internetNewsTable.setItem(selectedRow+1,1,QTableWidgetItem(newsDataSwapList[0]['title']))
                self.internetNewsTable.setItem(selectedRow,0,QTableWidgetItem(newsDataSwapList[1]['press']))
                self.internetNewsTable.setItem(selectedRow,1,QTableWidgetItem(newsDataSwapList[1]['title']))

                iTemp = iNewsList[selectedRow]
                iNewsList[selectedRow] = iNewsList[selectedRow+1]
                iNewsList[selectedRow+1] = iTemp

                self.internetNewsTable.selectRow(selectedRow+1)

                self.toMessage()
            except Exception as e:
                print('Error: '+str(e))

    def paperUp(self):
        selectedRow = self.paperNewsTable.currentRow()
        if selectedRow == 0:
            print('stopped')
        else:
            try:
                print('moved')
                newsDataSwapList = []

                press = self.paperNewsTable.item(selectedRow,0).text()
                title = self.paperNewsTable.item(selectedRow,1).text()
                newsData = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData)

                press = self.paperNewsTable.item(selectedRow-1,0).text()
                title = self.paperNewsTable.item(selectedRow-1,1).text()
                newsData2 = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData2)

                self.paperNewsTable.setItem(selectedRow-1,0,QTableWidgetItem(newsDataSwapList[0]['press']))
                self.paperNewsTable.setItem(selectedRow-1,1,QTableWidgetItem(newsDataSwapList[0]['title']))
                self.paperNewsTable.setItem(selectedRow,0,QTableWidgetItem(newsDataSwapList[1]['press']))
                self.paperNewsTable.setItem(selectedRow,1,QTableWidgetItem(newsDataSwapList[1]['title']))

                pTemp = pNewsList[selectedRow]
                pNewsList[selectedRow] = pNewsList[selectedRow-1]
                pNewsList[selectedRow-1] = pTemp

                self.paperNewsTable.selectRow(selectedRow-1)

                self.toMessage()
            except Exception as e:
                print('Error: '+str(e))

    def paperDown(self):
        selectedRow = self.paperNewsTable.currentRow()
        rowCount = self.paperNewsTable.rowCount()
        if selectedRow == -1 or selectedRow+1 == rowCount:
            print('stopped')
        else:
            try:
                print('moved')
                newsDataSwapList = []

                press = self.paperNewsTable.item(selectedRow,0).text()
                title = self.paperNewsTable.item(selectedRow,1).text()
                newsData = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData)

                press = self.paperNewsTable.item(selectedRow+1,0).text()
                title = self.paperNewsTable.item(selectedRow+1,1).text()
                newsData2 = {
                    'press' : press,
                    'title' : title,
                }
                newsDataSwapList.append(newsData2)

                self.paperNewsTable.setItem(selectedRow+1,0,QTableWidgetItem(newsDataSwapList[0]['press']))
                self.paperNewsTable.setItem(selectedRow+1,1,QTableWidgetItem(newsDataSwapList[0]['title']))
                self.paperNewsTable.setItem(selectedRow,0,QTableWidgetItem(newsDataSwapList[1]['press']))
                self.paperNewsTable.setItem(selectedRow,1,QTableWidgetItem(newsDataSwapList[1]['title']))

                pTemp = pNewsList[selectedRow]
                pNewsList[selectedRow] = pNewsList[selectedRow+1]
                pNewsList[selectedRow+1] = pTemp

                self.paperNewsTable.selectRow(selectedRow+1)

                self.toMessage()
            except Exception as e:
                print('Error: '+str(e))

    def toMessage(self):
        self.finalMessage.setText('')
        previewMessage = toMessage.toMessage(pNewsList,iNewsList)
        for i in range(len(previewMessage)):
            self.finalMessage.append(previewMessage[i])
        
    def exit(self) :
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()