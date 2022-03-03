import gspread as gspread

items_left_indent = 1
items_top_indent = 2

def get_sheets(googlesheet_id):
    gc = gspread.service_account(filename='serv_acc.json')

    sh = gc.open_by_key(googlesheet_id)

    return sh.worksheets()


def get_items(googlesheet_id, sheet: str):
    gc = gspread.service_account(filename='serv_acc.json')

    sh = gc.open_by_key(googlesheet_id)
    worksheet = sh.worksheet(sheet)
    values = worksheet.get_all_values()
    ret = []
    l = items_left_indent
    t = items_top_indent
    while values[t][l] != 'Итого':
        ret.append(values[t][l])
        t += 1
    return ret


def add_item_to_sheet(googlesheet_id, name, sheet, item):
    gc = gspread.service_account(filename='serv_acc.json')

    sh = gc.open_by_key(googlesheet_id)
    worksheet = sh.worksheet(sheet)
    cell = worksheet.find(name)
    col = cell.col
    values_list = worksheet.col_values(col)
    worksheet.update_cell(len(values_list) + 1, col, item)

if __name__ == '__main__':
    gc = gspread.service_account(filename='serv_acc.json')

    sh = gc.open_by_key('1fika6X6aCOBhUV882FoS897QrXmtSkxOdCQvrEXYitI')
    add_item_to_sheet('1fika6X6aCOBhUV882FoS897QrXmtSkxOdCQvrEXYitI', 'Саша', 'Расходники', 'предмет')


    print(sh)