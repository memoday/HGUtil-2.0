import win32com.client as win32  # 모듈 임포트
from datetime import date

today = date.today()
today= today.strftime("%Y.%m.%d.")

hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")  # 한/글 실행하기
hwp.XHwpWindows.Item(0).Visible = True  # 백그라운드 숨김 해제

hwp.HAction.GetDefault("ModifySection", hwp.HParameterSet.HSecDef.HSet)
hwp.HParameterSet.HSecDef.PageDef.LeftMargin = hwp.MiliToHwpUnit(20.0)
hwp.HParameterSet.HSecDef.PageDef.RightMargin = hwp.MiliToHwpUnit(20.0)
hwp.HParameterSet.HSecDef.PageDef.TopMargin = hwp.MiliToHwpUnit(15.0)
hwp.HParameterSet.HSecDef.PageDef.BottomMargin = hwp.MiliToHwpUnit(15.0)
hwp.HParameterSet.HSecDef.PageDef.HeaderLen = hwp.MiliToHwpUnit(10.0)
hwp.HParameterSet.HSecDef.PageDef.FooterLen = hwp.MiliToHwpUnit(10.0)
hwp.HParameterSet.HSecDef.HSet.SetItem("ApplyClass", 24)
hwp.HParameterSet.HSecDef.HSet.SetItem("ApplyTo", 2)
hwp.HAction.Execute("ModifySection", hwp.HParameterSet.HSecDef.HSet)

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

hwp.HAction.Run("ParagraphShapeAlignCenter")
hwp.HAction.Run("CharShapeHeightIncrease")
hwp.HAction.Run("CharShapeHeightIncrease")
hwpText('언론 모니터링\r\n')
hwp.HAction.Run("ParagraphShapeAlignRight")
hwpText(f'<{today}>')
fontBatang()
hwpText('\r\n')
hwp.HAction.Run("ParagraphShapeAlignJustify")
hwpText('※ 자세한 기사 내용을 보시려면 shift 키를 누른 채 아래의 기사 제목을 클릭하시면 새창으로 뜹니다.')
fontBatang()
hwpText('\r\n\r\n')

#표 양식 만들기
hwp.HAction.Run("CharShapeHeightDecrease")
hwp.HAction.Run("CharShapeHeightDecrease")
hwp.HAction.GetDefault("TableCreate", hwp.HParameterSet.HTableCreation.HSet)  # 표 생성 시작
hwp.HParameterSet.HTableCreation.Rows = 5  # 행 갯수
hwp.HParameterSet.HTableCreation.Cols = 4  # 열 갯수
hwp.HParameterSet.HTableCreation.WidthType = 2  # 너비 지정(0:단에맞춤, 1:문단에맞춤, 2:임의값)
hwp.HParameterSet.HTableCreation.HeightType = 1  # 높이 지정(0:자동, 1:임의값)
hwp.HParameterSet.HTableCreation.WidthValue = hwp.MiliToHwpUnit(169.0)  # 표 너비
hwp.HParameterSet.HTableCreation.HeightValue = hwp.MiliToHwpUnit(150.0)  # 표 높이
hwp.HParameterSet.HTableCreation.CreateItemArray("ColWidth", 4)  # 열 4개 생성
hwp.HParameterSet.HTableCreation.ColWidth.SetItem(0, hwp.MiliToHwpUnit(20.0))  # 1열
hwp.HParameterSet.HTableCreation.ColWidth.SetItem(1, hwp.MiliToHwpUnit(18.0))  # 2열
hwp.HParameterSet.HTableCreation.ColWidth.SetItem(2, hwp.MiliToHwpUnit(77.0))  # 3열
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
hwp.HParameterSet.HInsertText.Text = "신문/방송 보도사항"
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

newsInfo = []
newsInfo.append(('2023.2.14','KBS','테스트제목입니다',''))
newsInfo.append(('2023.2.15','SBS','테스트제목입니다2',''))

def fillData(date,press,title,summary):
    hwpText(date)
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")
    hwpText(press)
    hwp.HAction.Run("ParagraphShapeAlignCenter")
    hwp.HAction.Run("TableRightCell")
    hwpText(title)
    hwp.HAction.Run("ParagraphShapeAlignLeft")
    hwp.HAction.Run("TableRightCell")
    hwpText(summary)
    hwp.HAction.Run("ParagraphShapeAlignLeft")
    hwp.HAction.Run("TableCellBlockRow") #행 모두 선택
    fontDodum()
    hwp.HAction.Run("TableRightCell")

date, press, title, summary = newsInfo[0][0], newsInfo[0][1], newsInfo[0][2], newsInfo[0][3]
fillData(date,press,title,summary)
date, press, title, summary = newsInfo[1][0], newsInfo[1][1], newsInfo[1][2], newsInfo[1][3]
fillData(date,press,title,summary)