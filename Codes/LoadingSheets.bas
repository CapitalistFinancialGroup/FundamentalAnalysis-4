Attribute VB_Name = "Module1"

Dim warehouseID As String

Public Sub Main()
Dim tickerName As String, responseJSON As Object, Url As String, moneycontrolId As String, moneycontrolStock As String
Debug.Print "Starting Routinee"
tickerName = Worksheets("Introduction").Range("TickerName")
Set responseJSON = ParseJson(GetStockDetails(tickerName))
For Each Item In responseJSON
Url = Item("link_src")
Next
' Got stock id from moneycontrol
splittedUrl = Split(Url, "/")
moneycontrolId = splittedUrl(UBound(splittedUrl))
moneycontrolStock = splittedUrl(UBound(splittedUrl) - 1)


' Get warehouse id from the stock
warehouseID = getWareHouseID(tickerName)

' Create Balance Sheet
BalanceSheet moneycontrolStock, moneycontrolId

' Create Profit and Loss Statement
ProfitAndLoss moneycontrolStock, moneycontrolId

' Create Cash Flow Statement
CashFlow moneycontrolStock, moneycontrolId

' Create Financial Ratios
Financial_Ratio moneycontrolStock, moneycontrolId

' Create Investor Chart
Shareholder tickerName

' Create Peer Chart
Peer warehouseID

Debug.Print "Ending Routinee"
End Sub



Private Function GetStockDetails(stockName As String) As String
    Dim xmlhttp As New MSXML2.xmlhttp, myurl As String
    myurl = "https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=true&query=" + stockName + "&type=1&format=json"
    xmlhttp.Open "GET", myurl, False
    xmlhttp.Send
    GetStockDetails = xmlhttp.ResponseText
End Function

Sub Shareholder(stockName As String)
'
' shareholder Macro
'

'
    Url = "https://www.screener.in/company/" & stockName & "/consolidated/#shareholding"
    ' Deleting the Worksheet if present
    If Not GetWorksheet("Shareholder") Is Nothing Then
    Application.DisplayAlerts = False
    Worksheets("Shareholder").Delete
    Application.DisplayAlerts = True
    End If
    
    ' Deleting the Query connection if present
    find_used_connections ("Shareholder")
    
    ' Creating new worksheet and inserting the url
    Worksheets.Add(After:=Sheets(Sheets.Count)).Name = "Shareholder"
    Worksheets("Shareholder").Activate
    ActiveWorkbook.Queries.Add Name:="Shareholder", Formula:= _
        "let" & Chr(13) & "" & Chr(10) & "    Source = Web.Page(Web.Contents(""" & Url & """))," & Chr(13) & "" & Chr(10) & "    Data9 = Source{9}[Data]," & Chr(13) & "" & Chr(10) & "    #""Changed Type"" = Table.TransformColumnTypes(Data9,{{"""", type text}, {""Dec 2017"", type number}, {""Mar 2018"", type number}, {""Jun 2018"", type number}, {""Sep 2018"", type number}, {""Dec 2018"", type number}, " & _
        "{""Mar 2019"", type number}, {""Jun 2019"", type number}, {""Sep 2019"", type number}, {""Dec 2019"", type number}, {""Mar 2020"", type number}, {""Jun 2020"", type number}, {""Sep 2020"", type number}})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Changed Type"""
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""Table 9"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [Shareholder]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "Shareholder"
        .Refresh BackgroundQuery:=True
    End With
End Sub

Sub BalanceSheet(stockName As String, identifier As String)
'
' BalanceSheet Macro
'

'
    Url = "https://www.moneycontrol.com/financials/" & stockName & "/consolidated-balance-sheetVI/" & identifier & "#" + identifier
    ' Deleting the Worksheet if present
    If Not GetWorksheet("BalanceSheet") Is Nothing Then
    Application.DisplayAlerts = False
    Worksheets("BalanceSheet").Delete
    Application.DisplayAlerts = True
    End If
    
    ' Deleting the Query connection if present
    find_used_connections ("BalanceSheet")
    
    ' Creating new worksheet and inserting the url
    Worksheets.Add(After:=Sheets(Sheets.Count)).Name = "BalanceSheet"
    Worksheets("BalanceSheet").Activate
    ActiveWorkbook.Queries.Add Name:="BalanceSheet", Formula:= _
        "let" & Chr(13) & "" & Chr(10) & "    Source = Web.Page(Web.Contents(""" & Url & """ ))," & Chr(13) & "" & Chr(10) & "    Data0 = Source{0}[Data]," & Chr(13) & "" & Chr(10) & "    #""Changed Type"" = Table.TransformColumnTypes(Data0,{{""Column1"", type text}, {""Column2"", type text}, {""Column3"", type text}, {""Column4"", type text}, {""Column5"", type text}, {""Column6"", type te" & _
        "xt}, {""Column7"", type text}})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Changed Type"""
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""BalanceSheet"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [BalanceSheet]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "BalanceSheet"
        .Refresh BackgroundQuery:=True
    End With
End Sub


Private Sub find_used_connections(QueryName As String)
    For Each Item In ActiveWorkbook.Queries
        If Item.Name = QueryName Then
            Item.Delete
        End If
    Next Item

End Sub

Private Function GetWorksheet(shtName As String) As Worksheet
    On Error Resume Next
    Set GetWorksheet = Worksheets(shtName)
End Function

Private Function getWareHouseID(stockName As String) As String
    Dim xmlhttp As New MSXML2.xmlhttp, myurl As String, html As New HTMLDocument, topics As Object, topic As String, regex As Object, expectedString As Object, wId As Object
    myurl = "https://www.screener.in/company/" & stockName & "/consolidated/"
    xmlhttp.Open "GET", myurl, False
    xmlhttp.Send
    html.body.innerHTML = xmlhttp.ResponseText
    Set topics = html.getElementById("company-info")
    topic = topics.outerHTML
    Set regex = New RegExp
    regex.Pattern = "data-warehouse-id=""\d+"""
    Set expectedString = regex.Execute(topic)
    Debug.Assert expectedString.Count = 1
    regex.Pattern = "\d+"
    For Each Item In expectedString
        warehouseString = Item.Value
        Set wId = regex.Execute(warehouseString)
        Debug.Assert wId.Count = 1
        For Each id In wId
            getWareHouseID = id.Value
        Next id
    Next Item
End Function

Sub Peer(id As String)
'
' Peer Macro
'

'
   Url = "https://www.screener.in/api/company/" & id & "/peers/"
' Deleting the Worksheet if present
    If Not GetWorksheet("Peer") Is Nothing Then
    Application.DisplayAlerts = False
    Worksheets("Peer").Delete
    Application.DisplayAlerts = True
    End If
    
    ' Deleting the Query connection if present
    find_used_connections ("Peer")
    
    ' Creating new worksheet and inserting the url
    Worksheets.Add(After:=Sheets(Sheets.Count)).Name = "Peer"
    Worksheets("Peer").Activate
    ActiveWorkbook.Queries.Add Name:="Peer", Formula:= _
        "let" & Chr(13) & "" & Chr(10) & "    Source = Web.Page(Web.Contents(""" & Url & """))," & Chr(13) & "" & Chr(10) & "    Data0 = Source{0}[Data]," & Chr(13) & "" & Chr(10) & "    #""Changed Type"" = Table.TransformColumnTypes(Data0,{{""S.No."", Int64.Type}, {""Name"", type text}, {""CMP Rs."", type number}, {""P/E"", type number}, {""Mar Cap Rs.Cr."", type number}, {""Div Yld %"", Int64.Type}, {""NP Qtr Rs.Cr." & _
        """, type number}, {""Qtr Profit Var %"", type number}, {""Sales Qtr Rs.Cr."", type number}, {""Qtr Sales Var %"", type number}, {""ROCE %"", type number}})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Changed Type"""
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""Peer"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [Peer]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "Peer"
        .Refresh BackgroundQuery:=True
    End With
End Sub

Sub ProfitAndLoss(stockName As String, identifier As String)
'
' PL_16112020 Macro
'

'
' Deleting the Worksheet if present
    Url = "https://www.moneycontrol.com/financials/" & stockName & "/consolidated-profit-lossVI/" & identifier & "#" & identifier
    If Not GetWorksheet("P&L") Is Nothing Then
    Application.DisplayAlerts = False
    Worksheets("P&L").Delete
    Application.DisplayAlerts = True
    End If
    
    ' Deleting the Query connection if present
    find_used_connections ("PL")
    
    ' Creating new worksheet and inserting the url
    Worksheets.Add(After:=Sheets(Sheets.Count)).Name = "P&L"
    Worksheets("P&L").Activate
    ActiveWorkbook.Queries.Add Name:="PL", Formula:= _
        "let" & Chr(13) & "" & Chr(10) & "    Source = Web.Page(Web.Contents(""" & Url & """))," & Chr(13) & "" & Chr(10) & "    Data0 = Source{0}[Data]," & Chr(13) & "" & Chr(10) & "    #""Changed Type"" = Table.TransformColumnTypes(Data0,{{""Column1"", type text}, {""Column2"", type text}, {""Column3"", type text}, {""Column4"", type text}, {""Column5"", type text}, {""Column6"", type text" & _
        "}, {""Column7"", type text}})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Changed Type"""
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""PL"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [PL]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "PL"
        .Refresh BackgroundQuery:=True
    End With
End Sub

Sub Financial_Ratio(stockName As String, identifier As String)
'
'
'

'
   Url = "https://www.moneycontrol.com/financials/" & stockName & "/consolidated-ratiosVI/" & identifier & "#" & identifier
' Deleting the Worksheet if present
    If Not GetWorksheet("Ratio") Is Nothing Then
    Application.DisplayAlerts = False
    Worksheets("Ratio").Delete
    Application.DisplayAlerts = True
    End If
    
    ' Deleting the Query connection if present
    find_used_connections ("Ratio")
    
    ' Creating new worksheet and inserting the url
    Worksheets.Add(After:=Sheets(Sheets.Count)).Name = "Ratio"
    Worksheets("Ratio").Activate
    ActiveWorkbook.Queries.Add Name:="Ratio", Formula:= _
        "let" & Chr(13) & "" & Chr(10) & "    Source = Web.Page(Web.Contents(""" & Url & """))," & Chr(13) & "" & Chr(10) & "    Data0 = Source{0}[Data]," & Chr(13) & "" & Chr(10) & "    #""Promoted Headers"" = Table.PromoteHeaders(Data0, [PromoteAllScalars=true])," & Chr(13) & "" & Chr(10) & "    #""Changed Type"" = Table.TransformColumnTypes(#""Promoted Headers"",{{""Per Share Ratios"", type text}, {""Column2"", type numb" & _
        "er}, {""Column3"", type number}, {""Column4"", type number}, {""Column5"", type number}, {""Column6"", type number}, {"""", type text}})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Changed Type"""
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""Ratio"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [Ratio]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "Ratio"
        .Refresh BackgroundQuery:=True
    End With
    Range("A13").Select
    Selection.Style = "Accent6"
    Range("B13").Select
    Selection.Style = "Accent6"
    Selection.AutoFill Destination:=Range("B13:G13"), Type:=xlFillDefault
    Range("B13:G13").Select
    ActiveWindow.ScrollRow = 9
    ActiveWindow.ScrollRow = 10
    ActiveWindow.ScrollRow = 11
    ActiveWindow.ScrollRow = 12
    ActiveWindow.ScrollRow = 13
    ActiveWindow.ScrollRow = 12
    ActiveWindow.ScrollRow = 11
    ActiveWindow.ScrollRow = 12
    ActiveWindow.ScrollRow = 13
    Range("A24").Select
    Selection.Style = "Accent6"
    Range("B24").Select
    Selection.Style = "Accent6"
    Selection.AutoFill Destination:=Range("B24:G24"), Type:=xlFillDefault
    Range("B24:G24").Select
    ActiveWindow.ScrollRow = 14
    ActiveWindow.ScrollRow = 15
    ActiveWindow.ScrollRow = 16
    ActiveWindow.ScrollRow = 17
    ActiveWindow.ScrollRow = 18
    ActiveWindow.ScrollRow = 19
    ActiveWindow.ScrollRow = 20
    ActiveWindow.ScrollRow = 21
    ActiveWindow.ScrollRow = 22
    Range("A32").Select
    Selection.Style = "Accent6"
    Selection.AutoFill Destination:=Range("A32:G32"), Type:=xlFillDefault
    Range("A32:G32").Select
    Range("G32").Select
    ActiveCell.FormulaR1C1 = ""
    Range("F32").Select
    ActiveCell.FormulaR1C1 = ""
    Range("E32").Select
    ActiveCell.FormulaR1C1 = ""
    Range("D32").Select
    ActiveCell.FormulaR1C1 = ""
    Range("C32").Select
    ActiveCell.FormulaR1C1 = ""
    Range("B32").Select
    ActiveCell.FormulaR1C1 = ""
    Range("I22").Select
End Sub

Sub CashFlow(stockName As String, identifier As String)
'
' CashFlow Macro
'

'
' Deleting the Worksheet if present
    Url = "https://www.moneycontrol.com/financials/" & stockName & "/consolidated-cash-flowVI/" & identifier & "#" & identifier
    If Not GetWorksheet("CashFlow") Is Nothing Then
    Application.DisplayAlerts = False
    Worksheets("CashFlow").Delete
    Application.DisplayAlerts = True
    End If
    
    ' Deleting the Query connection if present
    find_used_connections ("CashFlow")
    
    ' Creating new worksheet and inserting the url
    Worksheets.Add(After:=Sheets(Sheets.Count)).Name = "CashFlow"
    Worksheets("CashFlow").Activate
    ActiveWorkbook.Queries.Add Name:="CashFlow", Formula:= _
        "let" & Chr(13) & "" & Chr(10) & "    Source = Web.Page(Web.Contents(""" & Url & """))," & Chr(13) & "" & Chr(10) & "    Data0 = Source{0}[Data]," & Chr(13) & "" & Chr(10) & "    #""Changed Type"" = Table.TransformColumnTypes(Data0,{{""Column1"", type text}, {""Column2"", type text}, {""Column3"", type text}, {""Column4"", type text}, {""Column5"", type text}, {""Column6"", type text" & _
        "}, {""Column7"", type text}})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Changed Type"""
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""CashFlow"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [CashFlow]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "CashFlow"
        .Refresh BackgroundQuery:=True
    End With
End Sub





