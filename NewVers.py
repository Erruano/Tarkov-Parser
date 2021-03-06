import re
import sys
import os
from PyQt5 import QtWidgets
import openpyxl
from win32com.client import DispatchEx
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import GUIs.MainWindow.gui as gui
import GUIs.process.processing as processing_window


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.operations()

    def operations(self):
        self.btn_refresh_price.clicked.connect(update_prices)
        self.btn_sort_crafts.clicked.connect(sort_crafts)
        self.btn_sort_barters.clicked.connect(sort_barters)
        self.btn_make_table.clicked.connect(make_table)
        self.btn_make_crafts.clicked.connect(update_crafts)
        self.btn_make_barters.clicked.connect(update_barters)
        self.btn_open_table.clicked.connect(open_table)


class ProcessWindow(QtWidgets.QMainWindow, processing_window.Ui_MainWindow):
    def __init__(self):
        super(ProcessWindow, self).__init__()
        self.setupUi(self)


def app():
    app_ = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app_.exec()


def process_window():
    app_ = QtWidgets.QApplication(sys.argv)
    window = ProcessWindow
    window.show()
    app_.exec()


def find_digit(a):
    num = ''
    for i in list(a):
        if i.isdigit():
            num += i
        elif i == '.':
            num += ','
    return num


def update_table():
    xlapp = DispatchEx("Excel.Application")
    wb = xlapp.Workbooks.Open(os.getcwd() + '\Database.xlsx')
    wb.RefreshAll()
    wb.Save()
    xlapp.Quit()


def isint(a):
    try:
        int(a)
        return True
    except ValueError:
        return False


def seek_price(request):
    wb = openpyxl.load_workbook('Database.xlsx')
    ws = wb['Prices']
    name = re.sub(r'\s+', ' ', request)
    for i in range(1, ws.max_row + 1):
        if ws.cell(row=i, column=1, ).value == name:
            return ws.cell(row=i, column=2).coordinate


def seek_vendor_price(request):
    wb = openpyxl.load_workbook('Database.xlsx')
    ws = wb['Prices']
    name = re.sub(r'\s+', ' ', request)
    for i in range(1, ws.max_row + 1):
        if ws.cell(row=i, column=1, ).value == name:
            return ws.cell(row=i, column=3).coordinate


def sort_items():
    update_table()
    try:
        df = pd.read_excel('Database.xlsx', sheet_name='Prices', engine='openpyxl')
    except ValueError:
        print("???????? 'Prices' ???? ????????????, ???????????????? ?????????????? 'update_prices'")
        update_prices()
        df = pd.read_excel("Database.xlsx", sheet_name="Prices", engine="openpyxl")
    sorted_df = df.sort_values(by="Instant Profit", ascending=False)
    wb = openpyxl.load_workbook("Database.xlsx")


def sort_crafts():
    update_table()
    # ??????????????????
    try:
        df = pd.read_excel('Database.xlsx', sheet_name='Crafts_raw', engine='openpyxl')
    except ValueError:
        print('???????? "Crafts_raw" ???? ????????????, ???????????????? ?????????????? "update_crafts"')
        update_crafts()
        df = pd.read_excel('Database.xlsx', sheet_name='Crafts_raw', engine='openpyxl')
    print('???????????????? ???? ???????????? ?????????????? ?????????? ?????????????????????? ?????????????? ???????????????? (Profit ?????? Profit/H)')
    by = str(input())
    sorted_df = df.sort_values(by=by, ascending=False)
    # ?????????????????? ???????????????????? + ?????????????? ????????????????
    wb = openpyxl.load_workbook('Database.xlsx')
    try:
        ws = wb["Crafts_nude"]
        for i in range(1, ws.max_row + 1):
            for y in range(1, ws.max_column + 1):
                ws.cell(row=i, column=y).value = None
        wb.save("Database.xlsx")
        wb = openpyxl.load_workbook("Database.xlsx")
        ws = wb["Crafts_nude"]
    except KeyError:
        ws = wb.create_sheet("Crafts_nude")
    for i in dataframe_to_rows(sorted_df, index=False, header=True):
        ws.append(i)
    wb.save('Database.xlsx')
    print("???????????? ??????????????????????????")


def sort_barters():
    update_table()
    # ??????????????????
    try:
        df = pd.read_excel('Database.xlsx', sheet_name='Barters_raw', engine='openpyxl')
    except ValueError:
        print('???????? "Barters_raw" ???? ????????????, ???????????????? ?????????????? "update_crafts"')
        update_barters()
        df = pd.read_excel('Database.xlsx', sheet_name='Barters_raw', engine='openpyxl')
    print('???????????????? ???? ???????????? ?????????????? ?????????? ?????????????????????? ?????????????? ???????????????? (Profit ?????? Instant Profit)')
    by = str(input())
    sorted_df = df.sort_values(by=by, ascending=False)
    # ?????????????????? ???????????????????? + ?????????????? ????????????????
    wb = openpyxl.load_workbook('Database.xlsx')
    try:
        ws = wb['Barters_nude']
        for i in range(1, ws.max_row + 1):
            for y in range(1, ws.max_column + 1):
                ws.cell(row=i, column=y).value = None
        wb.save("Database.xlsx")
        wb = openpyxl.load_workbook("Database.xlsx")
        ws = wb["Barters_nude"]
    except KeyError:
        ws = wb.create_sheet('Barters_nude')
    for i in dataframe_to_rows(sorted_df, index=False, header=True):
        ws.append(i)
    wb.save('Database.xlsx')
    print("???????????????????? ???????????????? ??????????????????")


def update_prices():
    driver_path = r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get('https://tarkov-market.com/ru/')
    driver.find_element(By.XPATH, '//div[@class="cell pointer"]').click()
    while True:
        try:
            driver.find_element(By.XPATH, '//span[text()=".300 AAC Blackout AP"]')
        except Exception:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            break
    names = driver.find_elements(By.XPATH, '//span[@class="name"]')
    pric = driver.find_elements(By.XPATH, '//span[@class="price-main"]')
    vendor = driver.find_elements(By.XPATH, '//div[@class="alt"]')

    df = pd.DataFrame()
    for i in range(len(names)):
        item = {'Name': names[i].text,
                'Price': pric[i].text,
                'Vendor Price': vendor[i].text,
                'Instant Profit': f'=C{str(i + 2)}-B{str(i + 2)}'}
        df = df.append(item, ignore_index=True)
    driver.quit()

    try:
        wb = openpyxl.load_workbook('Database.xlsx')
    except FileNotFoundError:
        wb = openpyxl.Workbook()
    try:
        ws = wb['Prices']
    except KeyError:
        ws = wb.active
        ws.title = 'Prices'
    for i in dataframe_to_rows(df, index=False, header=True):
        ws.append(i)
    wb.save('Database.xlsx')


def update_crafts():
    driver_path = r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get('https://tarkov-market.com/ru/hideout')
    while True:
        try:
            driver.find_element(By.XPATH, '//span[@class="big"][text()="???????????????????? ????-5"]')
        except Exception:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            break
    cards = driver.find_elements(By.XPATH, '//div[@class="card recipe"]')
    wb = openpyxl.load_workbook('Database.xlsx')
    try:
        ws = wb['Crafts_raw']
    except KeyError:
        ws = wb.create_sheet('Crafts_raw')
        column_names = ['Module', 'Ingredient', 'Amount', 'Price', 'Ingredient', 'Amount', 'Price', 'Ingredient',
                        'Amount', 'Price', 'Ingredient', 'Amount', 'Price', 'Ingredient', 'Amount', 'Price', 'Sum',
                        'Time(min)', 'Name', 'Amount', 'Price', 'Sum', 'Profit', 'Profit/H']
        for i in range(1, len(column_names) + 1):
            ws.cell(1, i, value=column_names[i - 1])
    row = 2
    for i in range(1, len(cards) + 1):
        column = 1
        ingredients = []
        in_amount = []
        pricescord = []
        names = driver.find_elements(By.XPATH, f'//div[@class="card recipe"][{i}]//span[@class="big"]')
        for y in range(1, len(names)):
            ingredients.append(driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//'
                                                             f'div[@class="d-flex only mb-15"][{y}]//span')
                               .get_attribute('textContent'))
            in_amount.append(driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//'
                                                           f'div[@class="d-flex only mb-15"][{y}]//'
                                                           f'div[@class="image"]/div').get_attribute('textContent'))
            pricescord.append(seek_price(driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//'
                                                                       f'div[@class="d-flex only mb-15"][{y}]//'
                                                                       f'span').get_attribute('textContent')))
        modules = driver.find_element(By.XPATH, f"//div[@class='row recipe'][{i}]//div[@class='big']").text
        result = driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"]'
                                               f'[{len(names)}]//span').get_attribute('textContent')
        time = list(driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//'
                                                  f'div[@class="text-center big"]').get_attribute('textContent'))
        minutes = 0
        tim = ''
        for t in range(len(time)):
            if isint(time[t]):
                tim += time[t]
            elif time[t] == '??':
                minutes = int(tim) * 60
                tim = ''
            elif time[t] == '??':
                minutes += int(tim)
                break
        result_amount = driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//'
                                                      f'div[@class="d-flex only mb-15"][{len(names)}]//'
                                                      f'div[@class="image"]/div').get_attribute('textContent')
        result_price_coordinate = seek_price(driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//div['
                                                                           f'@class="d-flex only mb-15"][{len(names)}'
                                                                           f']//span').get_attribute('textContent'))
        ws.cell(row=row, column=column, value=modules)
        column += 1
        for y in range(1, 6):
            try:
                ws.cell(row=row, column=column, value=ingredients[y - 1])
                column += 1
                ws.cell(row=row, column=column, value=find_digit(in_amount[y - 1]))
                column += 1
                ws.cell(row=row, column=column, value=f'=Prices!{pricescord[y - 1]}')
                column += 1
            except IndexError:
                column += 3
        ws.cell(row=row, column=column,
                value=f'=D{row}*C{row}+G{row}*F{row}+J{row}*I{row}+M{row}*L{row}+P{row}*O{row}')
        column += 1
        ws.cell(row=row, column=column, value=minutes)
        column += 1
        ws.cell(row=row, column=column, value=result)
        column += 1
        ws.cell(row=row, column=column, value=find_digit(result_amount))
        column += 1
        ws.cell(row=row, column=column, value=f'=Prices!{result_price_coordinate}')
        column += 1
        ws.cell(row=row, column=column, value=f'=U{row}*T{row}')
        column += 1
        ws.cell(row=row, column=column, value=f'=V{row}-Q{row}')
        column += 1
        ws.cell(row=row, column=column, value=f'=W{row}/R{row}*60')
        row += 1
    wb.save('Database.xlsx')
    driver.quit()


def update_barters():
    driver_path = r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get('https://tarkov-market.com/ru/barter')
    while True:
        try:
            driver.find_element(By.XPATH, '//span[@class="big"][text()="???????????????????? 6??43 6?? ??????????????-?? (0/85)"]')
        except Exception:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            break
    cards = driver.find_elements(By.XPATH, '//div[@class="card recipe"]')
    wb = openpyxl.load_workbook('Database.xlsx')
    try:
        ws = wb['Barters_raw']
    except KeyError:
        ws = wb.create_sheet('Barters_raw')
        columns = ['Module', 'Ingredient', 'Amount', 'Price', 'Ingredient', 'Amount', 'Price', 'Ingredient', 'Amount',
                   'Price', 'Ingredient', 'Amount', 'Price', 'Ingredient', 'Amount', 'Price', 'Sum', 'Name', 'Amount',
                   'Price', 'Vendor Price', 'Sum', 'Vendor Sum', 'Profit', 'Instant Profit']
        for i in range(1, len(columns) + 1):
            ws.cell(1, i, value=columns[i - 1])
    row = 2
    for i in range(1, len(cards) + 1):
        ingredients = []
        in_amount = []
        prices_coordinates = []
        trader = driver.find_element(By.XPATH, f'//div[@class="card recipe"][{i}]//div[@class="big"]').get_attribute(
            'textContent')
        names = driver.find_elements(By.XPATH, f'//div[@class="card recipe"][{i}]//span[@class="big"]')
        for y in range(1, len(names)):
            ingredients.append(driver.find_element(By.XPATH,
                                                   f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"][{y}]//span').get_attribute(
                'textContent'))
            in_amount.append(driver.find_element(By.XPATH,
                                                 f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"]{y}]//div[@class="image"]/div').get_attribute(
                'textContent'))
            prices_coordinates.append(seek_price(driver.find_element(By.XPATH,
                                                                     f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"][{y}]//span').get_attribute(
                'textContent')))
        result = driver.find_element(By.XPATH, '//div[@class="card recipe"][' + str(
            i) + ']//div[@class="d-flex only mb-15"][' + str(len(names)) + ']//span').get_attribute('textContent')
        result_amount = driver.find_element(By.XPATH,
                                            f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"][{len(names)}]//div[@class="image"]/div').get_attribute(
            'textContent')
        result_price_coordinate = seek_price(driver.find_element(By.XPATH,
                                                                 f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"][{len(names)}]//span').get_attribute(
            'textContent'))
        result_vendor_price_coordinate = seek_vendor_price(
            driver.find_element(By.XPATH,
                                f'//div[@class="card recipe"][{i}]//div[@class="d-flex only mb-15"][{len(names)}]//span').get_attribute(
                'textContent'))
        column = 1
        ws.cell(row=row, column=column, value=trader)
        column += 1
        for y in range(1, 6):
            try:
                ws.cell(row=row, column=column, value=ingredients[y - 1])
                column += 1
                ws.cell(row=row, column=column, value=find_digit(in_amount[y - 1]))
                column += 1
                ws.cell(row=row, column=column, value='=Prices!' + prices_coordinates[y - 1])
                column += 1
            except IndexError:
                column += 3
        ws.cell(row=row, column=column, value=f'=D{row}*C{row}+G{row}*F{row}+J{row}*I{row}+M{row}*L{row}+P{row}*O{row}')
        column += 1
        ws.cell(row=row, column=column, value=result)
        column += 1
        ws.cell(row=row, column=column, value=find_digit(result_amount))
        column += 1
        ws.cell(row=row, column=column, value=f'=Prices!{result_price_coordinate}')
        column += 1
        ws.cell(row=row, column=column, value=f'=Prices!{result_vendor_price_coordinate}')
        column += 1
        ws.cell(row=row, column=column, value=f'=S{row}*T{row}')
        column += 1
        ws.cell(row=row, column=column, value=f'=S{row}*U{row}')
        column += 1
        ws.cell(row=row, column=column, value=f'=V{row}-Q{row}')
        column += 1
        ws.cell(row=row, column=column, value=f'=W{row}-Q{row}')
        row += 1
    wb.save('Database.xlsx')
    driver.quit()


def make_table():
    wb = openpyxl.load_workbook('Database.xlsx')
    try:
        ws = wb['Crafts']
    except KeyError:
        ws = wb.create_sheet('Crafts')
        columns = ['Module', 'Ingredients', 'Amount', 'Price', 'Sum', 'Time(min)',
                   'Name', 'Amount', 'Price', 'Sum', 'Profit', 'Profit/H']
        for i in range(1, len(columns) + 1):
            ws.cell(1, i, value=columns[i - 1])
    row = 2
    for i in range(124):
        ws.cell(row=row, column=1, value=f'=Crafts_nude!A{i + 2}')
        ws.merge_cells(start_row=row, start_column=1, end_row=row + 4, end_column=1)
        for y in range(0, 5):
            ws.cell(row=row + y, column=2, value=f'=Crafts_nude!{str(chr(ord("B") + (y * 3))) + str(i + 2)}')
            ws.cell(row=row + y, column=3, value=f'=Crafts_nude!{str(chr(ord("C") + (y * 3))) + str(i + 2)}')
            ws.cell(row=row + y, column=4, value=f'=Crafts_nude!{str(chr(ord("D") + (y * 3))) + str(i + 2)}')
        ws.cell(row=row, column=5, value=f'=Crafts_nude!Q{i + 2}')
        ws.merge_cells(start_row=row, start_column=5, end_row=row + 4, end_column=5)
        ws.cell(row=row, column=6, value=f'=Crafts_nude!R{i + 2}')
        ws.merge_cells(start_row=row, start_column=6, end_row=row + 4, end_column=6)
        ws.cell(row=row, column=7, value=f'=Crafts_nude!S{i + 2}')
        ws.merge_cells(start_row=row, start_column=7, end_row=row + 4, end_column=7)
        ws.cell(row=row, column=8, value=f'=Crafts_nude!T{i + 2}')
        ws.merge_cells(start_row=row, start_column=8, end_row=row + 4, end_column=8)
        ws.cell(row=row, column=9, value=f'=Crafts_nude!U{i + 2}')
        ws.merge_cells(start_row=row, start_column=9, end_row=row + 4, end_column=9)
        ws.cell(row=row, column=10, value=f'=I{row}*H{row}')
        ws.merge_cells(start_row=row, start_column=10, end_row=row + 4, end_column=10)
        ws.cell(row=row, column=11, value=f'=J{row}-E{row}')
        ws.merge_cells(start_row=row, start_column=11, end_row=row + 4, end_column=11)
        ws.cell(row=row, column=12, value=f'=K{row}/F{row}*60')
        ws.merge_cells(start_row=row, start_column=12, end_row=row + 4, end_column=12)
        row += 5
    wb.save('Database.xlsx')


def make_barters_table():
    wb = openpyxl.load_workbook('Database.xlsx')
    try:
        ws = wb['Barters']
    except KeyError:
        ws = wb.create_sheet('Barters')
        columns = ['Module', 'Ingredients', 'Amount', 'Price', 'Sum', 'Name', 'Amount', 'Price', 'Sum', 'Profit']
        for i in range(1, len(columns) + 1):
            ws.cell(1, i, value=columns[i - 1])
    row = 2
    for i in range(124):
        ws.cell(row=row, column=1, value=f'=Barters_nude!A{str(i + 2)}')
        ws.merge_cells(start_row=row, start_column=1, end_row=row + 4, end_column=1)
        for y in range(0, 5):
            ws.cell(row=row + y, column=2, value=f'=Barters_nude!{chr(ord("B") + (y * 3)) + str(i + 2)}')
            ws.cell(row=row + y, column=3, value=f'=Barters_nude!{chr(ord("C") + (y * 3)) + str(i + 2)}')
            ws.cell(row=row + y, column=4, value=f'=Barters_nude!{chr(ord("D") + (y * 3)) + str(i + 2)}')
        ws.cell(row=row, column=5, value=f'=Barters_nude!Qstr{(i + 2)}')
        ws.merge_cells(start_row=row, start_column=5, end_row=row + 4, end_column=5)
        ws.cell(row=row, column=6, value=f'=Barters_nude!R{i + 2}')
        ws.merge_cells(start_row=row, start_column=6, end_row=row + 4, end_column=6)
        ws.cell(row=row, column=7, value=f'=Barters_nude!S{i + 2}')
        ws.merge_cells(start_row=row, start_column=7, end_row=row + 4, end_column=7)
        ws.cell(row=row, column=8, value=f'=Barters_nude!T{i + 2}')
        ws.merge_cells(start_row=row, start_column=8, end_row=row + 4, end_column=8)
        ws.cell(row=row, column=9, value=f'=G{row}*H{row}')
        ws.merge_cells(start_row=row, start_column=9, end_row=row + 4, end_column=9)
        ws.cell(row=row, column=10, value=f'=I{row}-E{row}')
        ws.merge_cells(start_row=row, start_column=10, end_row=row + 4, end_column=10)
        row += 5
    wb.save('Database.xlsx')


def open_table():
    path = 'Database.xlsx'
    os.system("start " + path)


if __name__ == '__main__':
    os.chdir('C:\Eruano\Programming\Tarkov Parser')
    app()

# TODO: ?????????????????????? ??????????????????:
#   ???????????????????? ??????
#   ?????????????????????? ???????????????????????????? (https://medium.com/nuances-of-programming/??????-????????????????-python-8df43f87ef6f)
#   ?????????????????? ?????????????? ?? headless ?????? ???????? ???????????????? ??????
# TODO: ?????????????? ?? ??????????????:
#   ???????????????? ????????
#   ?????????????? ?????????????????? ????????
# TODO: ?????????????????????????? ?????????????????? ????????????
# TODO: ?????????????????????? ?????????????????? ???????????? ?? ???????????????? ????????????????
# TODO: ???????????????? ?? ?????????????? ?????????????? ?????????????? ???? ?????????????? ????????????????
# TODO: ???????????????????????? pandas ?????????? ?????????????????? ?? ?????????????????? ??????????????
