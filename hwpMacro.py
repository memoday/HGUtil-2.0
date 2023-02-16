import win32com.client as win32  # 모듈 임포트
from datetime import date

today = date.today()
today= today.strftime("%Y.%m.%d.")

#한글 생성, 쪽 여백 등 기본 설정 및 헤더 생성 작업
def createHWP():
    global hwp
    global act
    global pset
    hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")  # 한/글 실행하기
    hwp.XHwpWindows.Item(0).Visible = True  # 백그라운드 숨김 해제

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
    hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1  # 글자처럼 취급
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
    hwpText(f'<{today} time>')
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
    try:
        hwp.HAction.GetDefault("TablePropertyDialog", hwp.HParameterSet.HShapeObject.HSet)
        hwp.HParameterSet.HShapeObject.HorzAlign = hwp.HAlign("Left")
        hwp.HParameterSet.HShapeObject.HSet.SetItem("ShapeType", 3)
        hwp.HParameterSet.HShapeObject.HSet.SetItem("ShapeCellSize", 0)
        hwp.HAction.Execute("TablePropertyDialog", hwp.HParameterSet.HShapeObject.HSet)
    except:
        pass

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
    hwp.HParameterSet.HTableCreation.RowHeight.SetItem(2, hwp.MiliToHwpUnit(16.0))  # 3행
    hwp.HParameterSet.HTableCreation.RowHeight.SetItem(3, hwp.MiliToHwpUnit(16.0))  # 4행
    hwp.HParameterSet.HTableCreation.RowHeight.SetItem(4, hwp.MiliToHwpUnit(16.0))  # 5행
    hwp.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1  # 글자처럼 취급
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
    hwpText(title)
    hwp.HAction.Run("ParagraphShapeAlignLeft")
    hwp.HAction.Run("TableRightCell")
    lineSpacing(100)
    hwpText(summary)
    hwp.HAction.Run("ParagraphShapeAlignLeft")
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
    scrapContent()
    hwpText("\r\n\r\n\r\n\r\n\r\n")

#메인 함수
def main(paperNewsList,internetNewsList):
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

