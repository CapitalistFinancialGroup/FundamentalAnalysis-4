Attribute VB_Name = "CashFlowAnalysis"
Sub Visualise_CashFlow()
    Dim RowForChart As Long, Row As Range, Row1 As Long, Row2 As Long, Row3 As Long, LastColumn
    ' Check if the sheet exists
    If GetWorksheet("CashFlow") Is Nothing Then
        Worksheets("Introduction").Range("B5") = "Cash Flow Statement not yet loaded. Try Later."
        Exit Sub
    End If
    
    ' Check if the sheet is loaded with the data
    Value = Worksheets("CashFlow").Range("A1")
    If InStr(Value, "Column") = 0 Then
        Worksheets("Introduction").Range("B5") = "Data Loading in Progress. Try Later."
        Exit Sub
    End If
    
    Worksheets("Introduction").Range("B5") = "Loading Visualization."
    ' Get Row Details to Create the line Charts
    RowForChart = GetLastRow("CashFlow") + 1
    LastColumn = GetLastColumn("CashFlow")
    With Worksheets("CashFlow").Range("A1:A" & RowForChart)
        Set Row = .Find("Operating Activities", LookIn:=xlValues, LookAt:=xlPart)
        Row1 = Row.Row
        Set Row = .Find("Investing Activities", LookIn:=xlValues, LookAt:=xlPart)
        Row2 = Row.Row
        Set Row = .Find("Financing Activities", LookIn:=xlValues, LookAt:=xlPart)
        Row3 = Row.Row
    End With
    
    'Create The Chart
    
End Sub
