# -*- coding:utf-8 -*-
import xlrd
from datetime import date, datetime
def read_excel():
    #  文件位置
    ExcelFile = xlrd.open_workbook('F:\Python\python3\python读取excel内容.xlsx')
    #  获取Excel文件sheet名
    print(ExcelFile.sheet_names())
    # ---------------------------
    # 若有多个sheet，则需要指定读取目标sheet例如读取sheet2
    # sheet2_name = ExcelFile.sheet_names()[1]
    # ---------------------------
    # 获取sheet内容（1.根据sheet索引，2.根据sheet名称）
    # sheet = ExcelFile.sheet_by_index(1)
    sheet = ExcelFile.sheet_by_name('Sheet1')
    # 打印sheet名称，行数，列数
    print(sheet.name, sheet.nrows, sheet.ncols)
    # 获取整行或整列的值
    rows = sheet.row_values(2)  # 第三行内容
    cols = sheet.col_values(1)  # 第2列内容
    print(rows, cols)
    rows = sheet.nrows
    # 获取单元格内容
    for i in range(0, rows):
        print('%s%s%s' % (sheet.cell(i, 0).value, '-' * 2, sheet.cell(i, 1).value))
    print('%s%s%s' % (sheet.cell(0, 0).value, '-'*2, sheet.cell(0, 1).value))
    print('%s%s%s' % (sheet.cell(1, 0).value, '-'*2, sheet.cell(1, 1).value))
    print('%s%s%s' % (sheet.cell(2, 0).value, '-'*2, sheet.cell(2, 1).value))
    print(sheet.cell_value(0, 0))
    print(sheet.cell_value(0, 1))
    print(sheet.cell_value(1, 0))
    print(sheet.cell_value(1, 1))
    print(sheet.row(0)[0].value)
    print(sheet.row(0)[1].value)
    print(sheet.row(1)[0].value)
    print(sheet.row(1)[1].value)
    # 打印单元格内容格式
    print(sheet.row(7)[0].value)
    print(sheet.cell(7, 0).ctype)
    print(sheet.cell(8, 0).ctype)
    print(sheet.cell(9, 0).ctype)
    print(sheet.cell(10, 0).ctype)
    print(sheet.cell(11, 0).ctype)
    print(sheet.cell(12, 0).ctype)
    print(sheet.cell(13, 0).ctype)
if __name__ == '__main__':
    read_excel()