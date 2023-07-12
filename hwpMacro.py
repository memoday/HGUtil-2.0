import win32com.client as win32  # 모듈 임포트
from datetime import date
import time
import os, sys, json
import requests
from PIL import Image
import shutil

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    if url != '':
        resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
        print('Original URL:'+resp.url)
        return resp.url
    else:
        return ''

#한글 생성, 쪽 여백 등 기본 설정 및 헤더 생성 작업
def createHWP():
    global hwp
    global act
    global pset
    hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")  # 한/글 실행하기
    hwp.XHwpWindows.Item(0).Visible = True  # 백그라운드 숨김 해제
    hwp.RegisterModule("FilePathCheckDLL","FilePathCheckerModule") # 보안모듈 추가, 레지스트리 작업 필요함

    act = hwp.CreateAction("ParagraphShape")  # 액션 생성 #linespacing을 위한 값
    pset = act.CreateSet()  # 파라미터셋 생성
    act.GetDefault(pset)  # 파라미터셋에 현재 상태값 채워넣기

    hwp.HAction.GetDefault("ModifySection", hwp.HParameterSet.HSecDef.HSet) #쪽 여백 설정
    hwp.HParameterSet.HSecDef.PageDef.LeftMargin = hwp.MiliToHwpUnit(20.0)
    hwp.HParameterSet.HSecDef.PageDef.RightMargin = hwp.MiliToHwpUnit(20.0)
    hwp.HParameterSet.HSecDef.PageDef.TopMargin = hwp.MiliToHwpUnit(15.0)
    hwp.HParameterSet.HSecDef.PageDef.BottomMargin = hwp.MiliToHwpUnit(15.0)
    hwp.HParameterSet.HSecDef.PageDef.HeaderLen = hwp.MiliToHwpUnit(10.0)
    hwp.HParameterSet.HSecDef.PageDef.FooterLen = hwp.MiliToHwpUnit(10.0)
    hwp.HParameterSet.HSecDef.HSet.SetItem("ApplyClass", 24)
    hwp.HParameterSet.HSecDef.HSet.SetItem("ApplyTo", 2)
    hwp.HAction.Execute("ModifySection", hwp.HParameterSet.HSecDef.HSet)

    hwp.HAction.Run("ParagraphShapeAlignCenter")

    #제목 표 만들기
    hwp.HAction.GetDefault("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  # 표 생성 시작
    hwp.HParameterSet.HTableCreation.Rows = 1  # 행 갯수
    hwp.HParameterSet.HTableCreation.Cols = 1  # 열 갯수
    hwp.HParameterSet.HTableCreation.WidthType = 2  # 너비 지정(0:단에맞춤, 1:문단에맞춤, 2:임의값)
    hwp.HParameterSet.HTableCreation.HeightType = 1  # 높이 지정(0:자동, 1:임의값)
    hwp.HParameterSet.HTableCreation.WidthValue = hwp.MiliToHwpUnit(100.0)  # 표 너비
    hwp.HParameterSet.HTableCreation.HeightValue = hwp.MiliToHwpUnit(15.0)  # 표 높이
    hwp.HParameterSet.HTableCreation.CreateItemArray("ColWidth", 1)  # 열 1개 생성
    hwp.HParameterSet.HTableCreation.ColWidth.SetItem(0, hwp.MiliToHwpUnit(103.0))  # 1열
    hwp.HParameterSet.HTableCreation.CreateItemArray("RowHeight", 1)  # 행 1개 생성
    hwp.HParameterSet.HTableCreation.RowHeight.SetItem(0, hwp.MiliToHwpUnit(15.0))  # 1행
    hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 0  # 글자처럼 취급
    hwp.HParameterSet.HTableCreation.TableProperties.Width = hwp.MiliToHwpUnit(100)
    hwp.HAction.Execute("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  # 위 코드 실행

    for i in range(20):
        hwp.HAction.Run("CharShapeHeightIncrease")

    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwpText("언론 모니터링")
    hwp.HAction.Run("TableCellBlockRow")
    fontHeadline()
    graphBorder()

    hwp.HAction.Run("Cancel")
    graphAlignCenter()

    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("CharShapeHeightIncrease")
    hwp.HAction.Run("CharShapeHeightIncrease")
    hwpText('\r\n')

    hwp.HAction.Run("ParagraphShapeAlignRight")

    today = date.today()
    today= today.strftime("%Y.%m.%d.")
    hours = int(time.strftime('%H'))

    if hours <= 12:
        reportHour = "09:00"
    else :
        reportHour = '17:00' 

    hwpText(f'<{today} {reportHour}>')
    fontBatang()
    hwpText('\r\n')
    hwp.HAction.Run("ParagraphShapeAlignJustify")
    lineSpacing(120)
    hwpText('※ 자세한 기사 내용을 보시려면 shift 키를 누른 채 아래의 기사 제목을 클릭하시면 새창으로 뜹니다.')
    fontBatang()
    hwpText('\r\n\r\n\r\n')

def hwpText(text):
    hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HParameterSet.HInsertText.Text = text
    hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)

def fontDodum():
    hwp.HAction.GetDefault("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HParameterSet.HCharShape.FaceNameUser = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeUser = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameSymbol = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeSymbol = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameOther = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeOther = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameJapanese = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeJapanese = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHanja = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeHanja = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameLatin = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeLatin = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHangul = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeHangul = hwp.FontType("TTF")
    hwp.HAction.Execute("CharShape", hwp.HParameterSet.HCharShape.HSet)

def fontBatang():
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.GetDefault("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HParameterSet.HCharShape.FaceNameUser = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeUser = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameSymbol = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeSymbol = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameOther = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeOther = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameJapanese = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeJapanese = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHanja = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeHanja = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameLatin = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeLatin = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHangul = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeHangul = hwp.FontType("TTF")
    hwp.HAction.Execute("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HAction.Run('Cancel')

def fontHeadline():
    hwp.HAction.GetDefault("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HParameterSet.HCharShape.FaceNameUser = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeUser = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameSymbol = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeSymbol = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameOther = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeOther = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameJapanese = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeJapanese = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHanja = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeHanja = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameLatin = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeLatin = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHangul = "HY헤드라인M"
    hwp.HParameterSet.HCharShape.FontTypeHangul = hwp.FontType("TTF")
    hwp.HAction.Execute("CharShape", hwp.HParameterSet.HCharShape.HSet)

def graphAlignCenter():
    shape_obejct = hwp.HParameterSet.HShapeObject
    hwp.HAction.GetDefault("TablePropertyDialog", shape_obejct.HSet)
    shape_obejct.HorzAlign = hwp.HAlign("Left")
    hwp.HAction.Execute("TablePropertyDialog", shape_obejct.HSet)


def graphBorder():
    hwp.HAction.GetDefault("CellBorder", hwp.HParameterSet.HCellBorderFill.HSet)
    hwp.HParameterSet.HCellBorderFill.BorderWidthBottom = hwp.HwpLineWidth("0.7mm")
    hwp.HParameterSet.HCellBorderFill.BorderTypeBottom = hwp.HwpLineType("SlimThick")
    hwp.HParameterSet.HCellBorderFill.BorderTypeTop = hwp.HwpLineType("None")
    hwp.HParameterSet.HCellBorderFill.BorderTypeRight = hwp.HwpLineType("None")
    hwp.HParameterSet.HCellBorderFill.BorderTypeLeft = hwp.HwpLineType("None")
    hwp.HAction.Execute("CellBorder", hwp.HParameterSet.HCellBorderFill.HSet)
    hwp.HAction.Run("Cancel")

def lineSpacing(value):
    pset.SetItem("LineSpacing", value)  # 줄간격을 value로 설정
    act.Execute(pset)  # 설정한 파라미터셋으로 액션 실행

def createTable(category,count): #category: 테이블명 count: 테이블별 행 개수
    #표 양식 만들기
    hwp.HAction.Run("CharShapeHeightDecrease")
    hwp.HAction.Run("CharShapeHeightDecrease")
    hwp.HAction.GetDefault("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  # 표 생성 시작
    hwp.HParameterSet.HTableCreation.Rows = 2+count  # 행 개수
    hwp.HParameterSet.HTableCreation.Cols = 4  # 열 개수
    hwp.HParameterSet.HTableCreation.WidthType = 2  # 너비 지정(0:단에맞춤, 1:문단에맞춤, 2:임의값)
    hwp.HParameterSet.HTableCreation.HeightType = 1  # 높이 지정(0:자동, 1:임의값)
    hwp.HParameterSet.HTableCreation.WidthValue = hwp.MiliToHwpUnit(169.0)  # 표 너비
    hwp.HParameterSet.HTableCreation.HeightValue = hwp.MiliToHwpUnit(150.0)  # 표 높이
    hwp.HParameterSet.HTableCreation.CreateItemArray("ColWidth", 4)  # 열 4개 생성
    hwp.HParameterSet.HTableCreation.ColWidth.SetItem(0, hwp.MiliToHwpUnit(21.0))  # 1열
    hwp.HParameterSet.HTableCreation.ColWidth.SetItem(1, hwp.MiliToHwpUnit(18.0))  # 2열
    hwp.HParameterSet.HTableCreation.ColWidth.SetItem(2, hwp.MiliToHwpUnit(76.0))  # 3열
    hwp.HParameterSet.HTableCreation.ColWidth.SetItem(3, hwp.MiliToHwpUnit(40.0))  # 4열
    hwp.HParameterSet.HTableCreation.CreateItemArray("RowHeight", 5)  # 행 5개 생성
    hwp.HParameterSet.HTableCreation.RowHeight.SetItem(0, hwp.MiliToHwpUnit(7.0))  # 1행
    hwp.HParameterSet.HTableCreation.RowHeight.SetItem(1, hwp.MiliToHwpUnit(7.0))  # 2행
    for i in range(count):
        hwp.HParameterSet.HTableCreation.RowHeight.SetItem(i+2, hwp.MiliToHwpUnit(15.0))  # 3행
    hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 0  # 글자처럼 취급
    hwp.HParameterSet.HTableCreation.TableProperties.Width = hwp.MiliToHwpUnit(148)  # 표 너비
    hwp.HAction.Execute("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  # 위 코드 실행

    hwp.HAction.Run("TableCellBlockRow")
    hwp.HAction.Run("TableMergeCell")
    hwp.HAction.Run("CharShapeBold")

    hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HParameterSet.HInsertText.Text = category
    hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableCellBlockRow")
    fontDodum()

    hwp.HAction.Run("TableRightCell")  # 우측셀로 이동
    hwp.HAction.Run("TableCellBlockRow") #2행 모두 선택
    fontDodum()
    hwp.HAction.Run("CharShapeBold")
    hwp.HAction.GetDefault("CellFill", hwp.HParameterSet.HCellBorderFill.HSet) #2행 배경색 칠하기
    hwp.HParameterSet.HCellBorderFill.FillAttr.type = hwp.BrushType("NullBrush|WinBrush")
    hwp.HParameterSet.HCellBorderFill.FillAttr.WinBrushFaceColor = hwp.RGBColor(153, 204, 2551)
    hwp.HParameterSet.HCellBorderFill.FillAttr.WinBrushHatchColor = hwp.RGBColor(153, 204, 2551)
    hwp.HParameterSet.HCellBorderFill.FillAttr.WinBrushFaceStyle = hwp.HatchStyle("None")
    hwp.HParameterSet.HCellBorderFill.FillAttr.WindowsBrush = 1
    hwp.HAction.Execute("CellFill", hwp.HParameterSet.HCellBorderFill.HSet)

    hwp.HAction.Run("TableColBegin") #2행 처음으로 돌아오기

    hwpText('일자')
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")  # 우측셀로 이동

    hwpText('언론사')
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")  # 우측셀로 이동

    hwpText('기사 제목')
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")  # 우측셀로 이동

    hwpText('주요내용')
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")

#표 아래 스크랩 내용 작성 함수
def scrapTitle():
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.GetDefault("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HParameterSet.HCharShape.FaceNameUser = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeUser = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameSymbol = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeSymbol = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameOther = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeOther = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameJapanese = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeJapanese = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHanja = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeHanja = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameLatin = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeLatin = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHangul = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeHangul = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.TextColor = hwp.RGBColor(0, 0, 255)
    hwp.HParameterSet.HCharShape.Height = hwp.PointToHwpUnit(21.0)
    hwp.HAction.Execute("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HAction.Run("CharShapeBold")
    hwp.HAction.Run('Cancel')

def scrapSub():
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.GetDefault("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HParameterSet.HCharShape.FaceNameUser = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeUser = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameSymbol = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeSymbol = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameOther = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeOther = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameJapanese = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeJapanese = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHanja = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeHanja = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameLatin = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeLatin = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHangul = "돋움"
    hwp.HParameterSet.HCharShape.FontTypeHangul = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.TextColor = hwp.RGBColor(60, 62, 64)
    hwp.HParameterSet.HCharShape.Height = hwp.PointToHwpUnit(12.0)
    hwp.HAction.Execute("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HAction.Run('Cancel')
    hwp.HAction.Run("CharShapeBold")

def scrapContent():
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.Run("Select")
    hwp.HAction.GetDefault("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HParameterSet.HCharShape.FaceNameUser = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeUser = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameSymbol = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeSymbol = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameOther = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeOther = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameJapanese = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeJapanese = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHanja = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeHanja = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameLatin = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeLatin = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.FaceNameHangul = "바탕"
    hwp.HParameterSet.HCharShape.FontTypeHangul = hwp.FontType("TTF")
    hwp.HParameterSet.HCharShape.TextColor = hwp.RGBColor(0, 0, 0)
    hwp.HParameterSet.HCharShape.Height = hwp.PointToHwpUnit(12.0)
    hwp.HAction.Execute("CharShape", hwp.HParameterSet.HCharShape.HSet)
    hwp.HAction.Run('Cancel')

#요약표 작성 함수
def fillData(date,press,title,summary):
    lineSpacing(100)
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwpText(date)
    hwp.HAction.Run("TableRightCell")
    lineSpacing(100)
    hwpText(press)
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")
    lineSpacing(100)
    hwp.HAction.Run("ParagraphShapeAlignLeft")
    hwpText(title)
    hwp.HAction.Run("TableRightCell")
    lineSpacing(100)
    hwp.HAction.Run("ParagraphShapeAlignLeft")
    if summary == "":
        # hwp.HAction.Run("TableCellBlock")
        # hwp.HAction.Run("TableCellBlockExtend")
        # hwp.HAction.Run("TableUpperCell")
        # hwp.HAction.Run("TableMergeCell")
        # hwp.HAction.Run("TableLowerCell")
        # hwp.HAction.Run("TableColBegin")
        hwpText('')
    else:
        hwpText(summary)
    hwp.HAction.Run("TableCellBlockRow") #행 모두 선택
    fontDodum()
    hwp.HAction.Run("TableRightCell")

def fillScrap(title,press,publishedDate,publishedTime,summary):
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwpText(title)
    scrapTitle()
    hwpText("\r\n")

    hwp.HAction.Run("ParagraphShapeAlignRight")
    hwpText(f'{press} {publishedDate} {publishedTime}')
    scrapSub()
    hwpText("\r\n\r\n")

    hwp.HAction.Run("ParagraphShapeAlignJustify")
    hwpText(summary)
    hwpText("\r\n\r\n\r\n\r\n\r\n\r\n")

def replaceImages(imageCode):
    try:
        for i in range(len(imageCode)):
            hwp.HAction.GetDefault("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
            hwp.HParameterSet.HFindReplace.ReplaceString = ""
            hwp.HParameterSet.HFindReplace.FindString = imageCode[i]
            hwp.HParameterSet.HFindReplace.IgnoreReplaceString = 0
            hwp.HParameterSet.HFindReplace.IgnoreFindString = 0
            hwp.HParameterSet.HFindReplace.Direction = hwp.FindDir("AllDoc")
            hwp.HParameterSet.HFindReplace.WholeWordOnly = 0
            hwp.HParameterSet.HFindReplace.UseWildCards = 0
            hwp.HParameterSet.HFindReplace.SeveralWords = 0
            hwp.HParameterSet.HFindReplace.AllWordForms = 0
            hwp.HParameterSet.HFindReplace.MatchCase = 0
            hwp.HParameterSet.HFindReplace.ReplaceMode = 0
            hwp.HParameterSet.HFindReplace.ReplaceStyle = ""
            hwp.HParameterSet.HFindReplace.FindStyle = ""
            hwp.HParameterSet.HFindReplace.FindRegExp = 0
            hwp.HParameterSet.HFindReplace.FindJaso = 0
            hwp.HParameterSet.HFindReplace.HanjaFromHangul = 0
            hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
            hwp.HParameterSet.HFindReplace.FindType = 1
            hwp.HAction.Execute("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
            hwpText('\r\n')
            try:
                image_path = os.getcwd() + f'\HGUtil_images\{imageCode[i]}.jpg'
                hwp.InsertPicture(image_path)
                print(os.path.exists(image_path))
                print(f'이미지를 첨부했습니다 {imageCode[i]}')
            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)

def saveAs():
    filename = '한강관련 주요보도사항_'
    extension ='.hwpx'

    today = time.strftime('%y.%m.%d.') 
    hours = int(time.strftime('%H'))

    if hours <= 12:
        reportHour = "09"
    else :
        reportHour = '17'

    filename = filename+f'{today}{reportHour}시'
    checkFileExists = os.path.join(os.getcwd(), filename + extension)
    
    if os.path.exists(checkFileExists):
        print('지정된 경로에 동일 명의 파일이 존재해 저장을 중단했습니다.')
        return
    else:
        pass

    hwp.SaveAs(os.path.join(os.getcwd(), filename + extension))

#메인 함수
def main(paperNewsList,internetNewsList,finalNewsList):

    long_url = []
    imageCode = []
    
    #이미지 데이터 처리하는 과정
    for i in range(len(finalNewsList)):
        long_url.append(get_real_url_from_shortlink(finalNewsList[i]['shortenUrl']))
    
    # with open('image_dict.json', 'r') as f:
    #     image_json = json.load(f)

    # for i in range(len(long_url)):
    #     jsonKeys = image_json.keys()
    #     if long_url[i] in jsonKeys:
    #         print(long_url[i])
    #         for key in image_json[long_url[i]].keys():
    #             print(key)
    #             imageCode.append(key)

    if not os.path.exists("HGUtil_images"):
        os.makedirs("HGUtil_images")

    with open('image_dict.json', 'r') as f:
        image_json = json.load(f)

    for i in range(len(long_url)):
        jsonKeys = image_json.keys()
        if long_url[i] in jsonKeys:
            print(f'입력한 키: {long_url[i]}')
            for verificationCode in image_json[long_url[i]].keys():
                print(f'반환된 값: {verificationCode}')

                imageCode.append(verificationCode)
                image_url = image_json[long_url[i]][verificationCode]
                reponse = requests.get(image_url) #인식된 image 다운로드
                with open(f'HGUtil_images/{verificationCode}.jpg','wb') as f:
                    f.write(reponse.content)
                try: #다운 받은 이미지의 크기를 조정함
                    with Image.open(f'HGUtil_images/{verificationCode}.jpg') as downloadImage:
                        # Change the size while preserving the aspect ratio
                        width, height = downloadImage.size
                        if width >= 350:
                            ratio = width / 350
                            new_size = (int(width / ratio), int(height / ratio))
                            downloadImage = downloadImage.resize(new_size, resample=Image.BICUBIC)

                            # Save the updated image with original quality
                            downloadImage.save(f'HGUtil_images/{verificationCode}.jpg', quality=95)
                        else:
                            print(f"Image {verificationCode} is too small to resize.")
                except Exception as e:
                    print(e)
                    print('이미지 크기 조정 과정에서 오류가 발생했습니다.')

    #한글 생성
    createHWP()
    if len(paperNewsList) > 0:
        createTable(category="신문/방송 보도사항", count=len(paperNewsList))
        for i in range(len(paperNewsList)):
            publishedDate, press, title,url, summary = paperNewsList[i]['publishedDate'], paperNewsList[i]['press'], paperNewsList[i]['title'], paperNewsList[i]['shortenUrl'], paperNewsList[i]['summary']
            if url == '':
                title = str(title)
            else:
                title = str(title+"\r\n"+url)
            fillData(publishedDate,press,title,summary)
        hwp.MovePos(3)
        hwpText('\r\n\r\n')
    if len(internetNewsList) > 0:
        createTable(category="인터넷 보도사항", count=len(internetNewsList))
        for i in range(len(internetNewsList)):
            publishedDate, press, title, url, summary = internetNewsList[i]['publishedDate'], internetNewsList[i]['press'], internetNewsList[i]['title'], internetNewsList[i]['shortenUrl'], internetNewsList[i]['summary']
            if url == '':
                title = str(title)
            else:
                title = str(title+"\r\n"+url)
            fillData(publishedDate,press,title,summary)
    hwp.MovePos(3)

    if len(paperNewsList) > 0:
        hwp.HAction.Run("BreakPage")
        for i in range(len(paperNewsList)):
            title, press, publishedDate, publishedTime,content = paperNewsList[i]['title'], paperNewsList[i]['press'], paperNewsList[i]['publishedDate'], paperNewsList[i]['publishedTime'], paperNewsList[i]['content']
            fillScrap(title, press, publishedDate, publishedTime,content)
        hwp.MovePos(3)
    if len(internetNewsList) > 0:
        hwp.HAction.Run("BreakPage")
        for i in range(len(internetNewsList)):
            title, press, publishedDate, publishedTime,content = internetNewsList[i]['title'], internetNewsList[i]['press'], internetNewsList[i]['publishedDate'], internetNewsList[i]['publishedTime'], internetNewsList[i]['content']
            fillScrap(title, press, publishedDate, publishedTime,content)
    
    print('hwpMacro 이미지 첨부를 시작합니다')
    replaceImages(imageCode)

    image_folder_path = os.getcwd() + '\HGUtil_images'

    if os.path.exists(image_folder_path):
        shutil.rmtree(image_folder_path)
        print(f"Folder {image_folder_path} and its contents have been deleted.")
    else:
        print(f"Folder {image_folder_path} does not exist.")
    saveAs()
    print('hwpMacro 작업이 끝났습니다')

def exportSummary(paperNewsList,internetNewsList,finalNewsList):
    #한글 생성
    createHWP()
    if len(paperNewsList) > 0:
        createTable(category="신문/방송 보도사항", count=len(paperNewsList))
        for i in range(len(paperNewsList)):
            publishedDate, press, title,url, summary = paperNewsList[i]['publishedDate'], paperNewsList[i]['press'], paperNewsList[i]['title'], paperNewsList[i]['shortenUrl'], paperNewsList[i]['summary']
            if url == '':
                title = str(title)
            else:
                title = str(title+"\r\n"+url)
            fillData(publishedDate,press,title,summary)
        hwp.MovePos(3)
        hwpText('\r\n\r\n')
    if len(internetNewsList) > 0:
        createTable(category="인터넷 보도사항", count=len(internetNewsList))
        for i in range(len(internetNewsList)):
            publishedDate, press, title, url, summary = internetNewsList[i]['publishedDate'], internetNewsList[i]['press'], internetNewsList[i]['title'], internetNewsList[i]['shortenUrl'], internetNewsList[i]['summary']
            if url == '':
                title = str(title)
            else:
                title = str(title+"\r\n"+url)
            fillData(publishedDate,press,title,summary)
    
    print('hwpMacro 작업이 끝났습니다')

def exportSelectionSummary(paperNewsList,internetNewsList,finalNewsList):

    long_url = []
    imageCode = []
    
    #이미지 데이터 처리하는 과정
    for i in range(len(finalNewsList)):
        long_url.append(get_real_url_from_shortlink(finalNewsList[i]['shortenUrl']))

    if not os.path.exists("HGUtil_images"):
        os.makedirs("HGUtil_images")

    with open('image_dict.json', 'r') as f:
        image_json = json.load(f)

    for i in range(len(long_url)):
        jsonKeys = image_json.keys()
        if long_url[i] in jsonKeys:
            print(f'입력한 키: {long_url[i]}')
            for verificationCode in image_json[long_url[i]].keys():
                print(f'반환된 값: {verificationCode}')

                imageCode.append(verificationCode)
                image_url = image_json[long_url[i]][verificationCode]
                reponse = requests.get(image_url) #인식된 image 다운로드
                with open(f'HGUtil_images/{verificationCode}.jpg','wb') as f:
                    f.write(reponse.content)
                try: #다운 받은 이미지의 크기를 조정함
                    with Image.open(f'HGUtil_images/{verificationCode}.jpg') as downloadImage:
                        # Change the size while preserving the aspect ratio
                        width, height = downloadImage.size
                        if width >= 350:
                            ratio = width / 350
                            new_size = (int(width / ratio), int(height / ratio))
                            downloadImage = downloadImage.resize(new_size, resample=Image.BICUBIC)

                            # Save the updated image with original quality
                            downloadImage.save(f'HGUtil_images/{verificationCode}.jpg', quality=95)
                        else:
                            print(f"Image {verificationCode} is too small to resize.")
                except Exception as e:
                    print(e)
                    print('이미지 크기 조정 과정에서 오류가 발생했습니다.')

    #한글 생성
    createHWP()
    if len(paperNewsList) > 0:
        createTable(category="신문/방송 보도사항", count=len(paperNewsList))
        for i in range(len(paperNewsList)):
            publishedDate, press, title,url, summary = paperNewsList[i]['publishedDate'], paperNewsList[i]['press'], paperNewsList[i]['title'], paperNewsList[i]['shortenUrl'], paperNewsList[i]['summary']
            title = str(title+"\r\n"+url)
            fillData(publishedDate,press,title,summary)
        hwp.MovePos(3)
        hwpText('\r\n\r\n')
    if len(internetNewsList) > 0:
        createTable(category="인터넷 보도사항", count=len(internetNewsList))
        for i in range(len(internetNewsList)):
            publishedDate, press, title, url, summary = internetNewsList[i]['publishedDate'], internetNewsList[i]['press'], internetNewsList[i]['title'], internetNewsList[i]['shortenUrl'], internetNewsList[i]['summary']
            title = str(title+"\r\n"+url)
            fillData(publishedDate,press,title,summary)
    hwp.MovePos(3)

    if len(paperNewsList) > 0:
        hwp.HAction.Run("BreakPage")
        for i in range(len(paperNewsList)):
            title, press, publishedDate, publishedTime,content = paperNewsList[i]['title'], paperNewsList[i]['press'], paperNewsList[i]['publishedDate'], paperNewsList[i]['publishedTime'], paperNewsList[i]['content']
            fillScrap(title, press, publishedDate, publishedTime,content)
        hwp.MovePos(3)
    if len(internetNewsList) > 0:
        hwp.HAction.Run("BreakPage")
        for i in range(len(internetNewsList)):
            title, press, publishedDate, publishedTime,content = internetNewsList[i]['title'], internetNewsList[i]['press'], internetNewsList[i]['publishedDate'], internetNewsList[i]['publishedTime'], internetNewsList[i]['content']
            fillScrap(title, press, publishedDate, publishedTime,content)
    
    print('hwpMacro 이미지 첨부를 시작합니다')
    replaceImages(imageCode)

    image_folder_path = os.getcwd() + '\HGUtil_images'

    if os.path.exists(image_folder_path):
        shutil.rmtree(image_folder_path)
        print(f"Folder {image_folder_path} and its contents have been deleted.")
    else:
        print(f"Folder {image_folder_path} does not exist.")
    print('hwpMacro 작업이 끝났습니다')