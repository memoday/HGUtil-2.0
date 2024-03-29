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
import webbrowser
from PyQt5.QtCore import Qt

__version__ = 'v1.3.6'

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

        self.btn_addNews.clicked.connect(self.runCrawl)
        self.btn_hwp.clicked.connect(self.exportHangul)
        self.btn_message.clicked.connect(self.exportMessage)
        self.input_link.returnPressed.connect(self.addNews)
        self.btn_save.clicked.connect(self.save)
        self.btn_load.clicked.connect(self.load)
        self.btn_summary.clicked.connect(self.exportSummary)
        self.btn_selectionSummary.clicked.connect(self.exportSelectionSummary)
        self.btn_manualAdd.clicked.connect(self.manualAdd)
        
        self.autoStart.setChecked(True)
        self.doubleClickWeb.setChecked(True)

        header = self.newsTable.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Stretch)

        self.newsTable.setStyleSheet("QTableView::item:selected { background-color: #FFD700; }")
        self.btn_delete.clicked.connect(self.deleteRow)
        self.newsTable.doubleClicked.connect(self.on_double_click)


    def manualAdd(self):
        self.combo = QComboBox() #신문/방송 or 인터넷 콤보박스 추가
        self.combo.addItem("신문/방송")
        self.combo.addItem("인터넷")
        self.combo.setCurrentIndex(1)

        row_index = self.newsTable.rowCount()
        self.newsTable.insertRow(row_index)

        self.checkbox = QCheckBox()

        self.newsTable.setCellWidget(row_index,0,self.checkbox)
        self.newsTable.setCellWidget(row_index,1,self.combo)
        self.newsTable.setItem(row_index,2,QTableWidgetItem(''))
        self.newsTable.setItem(row_index,3,QTableWidgetItem(''))
        self.newsTable.setItem(row_index,4,QTableWidgetItem(''))
        self.newsTable.setItem(row_index,5,QTableWidgetItem(''))
        self.newsTable.setItem(row_index,6,QTableWidgetItem(''))
        self.newsTable.setItem(row_index,7,QTableWidgetItem(''))

    def on_double_click(self):
        if self.doubleClickWeb.isChecked() == True:
            for idx in self.newsTable.selectionModel().selectedIndexes():
                    row_number = idx.row()
                    column_number = idx.column()
                    if column_number == 7: #더블클릭한 열이 7번째 열일 경우(주소)
                        cellValue = self.newsTable.item(row_number,column_number).text()
                        print(f'브라우저로 {cellValue}에 접속합니다. 테이블 좌표: ({row_number},{column_number})')
                        try:
                            webbrowser.open_new_tab(cellValue)
                        except:
                            print('URL 오류로 인해 작업을 취소합니다.')
                            return
                    else:
                        pass

    def runCrawl(self):
        if self.autoStart.isChecked() == True:
            copied = app.clipboard().text()
            self.input_link.setText(copied)
            WindowClass.addNews(self)
        else:
            WindowClass.addNews(self)

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

                    self.checkbox = QCheckBox()

                    self.newsTable.setCellWidget(row_index,0,self.checkbox)
                    self.newsTable.setCellWidget(row_index,1,self.combo)
                    self.newsTable.setItem(row_index,2,QTableWidgetItem(publishedDateTime))
                    self.newsTable.setItem(row_index,3,QTableWidgetItem(press))
                    self.newsTable.setItem(row_index,4,QTableWidgetItem(title))
                    self.newsTable.setItem(row_index,5,QTableWidgetItem(content))
                    self.newsTable.setItem(row_index,6,QTableWidgetItem(summary))
                    self.newsTable.setItem(row_index,7,QTableWidgetItem(shortenUrl))

                self.statusBar().showMessage(f"기사를 등록했습니다. ({press})")
                newsList.clear()
                input_link.clear()
            
            else:
                pass
        except Exception as e:
            self.statusBar().showMessage("[오류] "+str(e))
        self.newsTable.setSortingEnabled(True)

    def exportHangul(self):
        try:
            rows = self.newsTable.rowCount()
            columns = self.newsTable.columnCount()

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
                    self.statusBar().showMessage('[오류] 날짜가 입력되지 않은 기사가 있습니다.')
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
            
            if len(finalNewsList) <= 0:
                self.statusBar().showMessage('선택된 기사가 없습니다.')
                return
            else:
                for i in range(len(finalNewsList)):
                    if finalNewsList[i]["newsType"] == "신문/방송":
                        paperNewsList.append(finalNewsList[i])
                    elif finalNewsList[i]["newsType"] == "인터넷":
                        internetNewsList.append(finalNewsList[i])

                hwpMacro.main(paperNewsList,internetNewsList,finalNewsList)
        except Exception as e:
            self.statusBar().showMessage("[오류] "+str(e))

    def exportMessage(self):
        try:
            rows = self.newsTable.rowCount()
            columns = self.newsTable.columnCount()

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
                    if totalNewsList[i]['summary'] == '':
                        self.statusBar().showMessage(f"[오류] 주요내용이 누락됐습니다. {totalNewsList[i]['title']}")
                        return
                    elif totalNewsList[i]['shortenUrl'] == '':
                        self.statusBar().showMessage(f"[오류] 주소가 누락됐습니다. {totalNewsList[i]['title']}")
                        return
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
            self.statusBar().showMessage("[오류] "+str(e))

    def exportSummary(self):
        try:
            rows = self.newsTable.rowCount()
            columns = self.newsTable.columnCount()

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
                    self.statusBar().showMessage('[오류] 날짜가 입력되지 않은 기사가 있습니다.')
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

                finalNewsList.append(news)
            
            if len(finalNewsList) <= 0:
                self.statusBar().showMessage('[오류] 선택된 기사가 없습니다.')
                return
            else:
                for i in range(len(finalNewsList)):
                    if finalNewsList[i]["newsType"] == "신문/방송":
                        paperNewsList.append(finalNewsList[i])
                    elif finalNewsList[i]["newsType"] == "인터넷":
                        internetNewsList.append(finalNewsList[i])

                hwpMacro.exportSummary(paperNewsList,internetNewsList,finalNewsList)

        except Exception as e:
            self.statusBar().showMessage("[오류] "+str(e))

    def exportSelectionSummary(self):
        try:
            rows = self.newsTable.rowCount()
            columns = self.newsTable.columnCount()

            finalNewsList = []
            paperNewsList = []
            internetNewsList = []
            for i in range(rows):
                checked = self.newsTable.cellWidget(i,0).isChecked()
                if not checked:
                    continue
                newsType = self.newsTable.cellWidget(i,1).currentText() #table데이터를 배열화하는 작업
                publishedDateTime = self.newsTable.item(i,2).text()
                press = self.newsTable.item(i,3).text()
                title = self.newsTable.item(i,4).text()
                content = self.newsTable.item(i,5).text()
                summary = self.newsTable.item(i,6).text()
                shortenUrl = self.newsTable.item(i,7).text()

                if publishedDateTime == "":
                    self.statusBar().showMessage('[오류] 날짜가 입력되지 않은 기사가 있습니다.')
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

                finalNewsList.append(news)
            
            if len(finalNewsList) <= 0:
                self.statusBar().showMessage('[오류] 선택된 기사가 없습니다.')
                return
            else:
                for i in range(len(finalNewsList)):
                    if finalNewsList[i]["newsType"] == "신문/방송":
                        paperNewsList.append(finalNewsList[i])
                    elif finalNewsList[i]["newsType"] == "인터넷":
                        internetNewsList.append(finalNewsList[i])

                hwpMacro.exportSelectionSummary(paperNewsList,internetNewsList,finalNewsList)
                
        except Exception as e:
            self.statusBar().showMessage("[오류] "+str(e))

    def deleteRow(self):
        selected = self.newsTable.currentRow()
        if selected >= 0:
            self.newsTable.removeRow(selected)
            self.statusBar().showMessage(f"{selected+1}번째 행을 삭제했습니다.")
            self.newsTable.setCurrentItem(None) 
        else:
            self.statusBar().showMessage("삭제할 기사를 선택해주세요.")

    def save(self):
        settings = QSettings("table.ini", QSettings.IniFormat)
        rowCount = self.newsTable.rowCount()
        if rowCount == 0:
            self.statusBar().showMessage('저장할 데이터가 없습니다.')
            return
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
        savedTime = datetime.now().replace(microsecond=0)
        savedTime = savedTime.strftime("%H:%M:%S")
        print(savedTime)
        self.statusBar().showMessage('현재 테이블이 table.ini에 저장됐습니다. '+str(savedTime))
    
    def load(self):
        try: 
            if self.newsTable.rowCount() > 0: #테이블이 비어있지 않은 경우 경고창 표시
                warning_msgBox = QMessageBox()
                reply = warning_msgBox.warning(self, '경고', '현재 작업 중인 테이블이 사라집니다. \n그래도 진행하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    pass
                else:
                    return
            
            settings = QSettings("table.ini", QSettings.IniFormat)
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
            self.statusBar().showMessage(f'기사 {len(ini)}건을 불러왔습니다.')
        except Exception as e:
            self.statusBar().showMessage('[오류] '+str(e))

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.save()

    def closeEvent(self, event):
        sys.exit(0)


class messageWindow(QDialog,form_messageWindow):
    
    def __init__(self,paperNewsList,internetNewsList):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(icon))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

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