Attribute VB_Name = "Utilities"
Function GetWorksheet(shtName As String) As Worksheet
    On Error Resume Next
    Set GetWorksheet = Worksheets(shtName)
End Function

Function GetLastRow(shtName As String)
    GetLastRow = Worksheets(shtName).Cells(Rows.Count, 1).End(xlUp).Row
End Function

Function GetLastColumn(shtName As String)
    GetLastColumn = Worksheets(shtName).Cells(1, Columns.Count).End(xlToLeft).Column
End Function
