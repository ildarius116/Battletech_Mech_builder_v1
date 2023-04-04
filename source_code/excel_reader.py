import xlrd


def main(search_list):
    weapon_type_list = []
    template_list1 = ['Type', 'Class', 'Designation', 'Modification', 'Tonnage', 'Shots', 'DMG_Single', 'Heat',
                     'Ammo_Rounds', 'DMG_Full', 'DMG/Tonn', 'Heatsinks', 'Ammo_Tonns', 'Full_Weight']
    template_list = ['T', 'C', 'D', 'M', 'W', 'S', 'DS', 'H', 'AR', 'DF', 'DT', 'HS', 'AT', 'FW']
    empty_dict = {'T': ' ', 'C': ' ', 'D': ' ', 'M': ' ', 'W': 0, 'S': 0, 'DS': 0, 'H': 0, 'AR': 0,
                  'DF': 0, 'DT': 0, 'HS': 0, 'AT': 0, 'FW': 0}

    """ Получение списка из экселя """
    workbook = xlrd.open_workbook("BattleTech Weapon Efficiency.xlsx")
    worksheet = workbook.sheet_by_index(0)
    income_list = []
    for i in range(3, 102):  # количество считываемых строк таблицы
        tmp_list = []
        for j in range(1, 15):  # количество считываемых столбцов таблицы
            value = worksheet.cell_value(i, j)
            if isinstance(value, float):
                tmp_list.append(round(value, 1))
            else:
                tmp_list.append(value)
        income_list.append(tmp_list)

    """ Преобразование списка из экселя в библиотеку """
    weapon_list = []
    prev_value = ''
    search_list = search_list[1:-1]
    # print(f'search_list = {search_list}')
    for item in income_list:
        tmp_dict = dict(zip(template_list, item))
        # print(f'tmp_dict = {tmp_dict}')
        if tmp_dict['T'] != prev_value:
            prev_value = tmp_dict['T']
            empty_dict['T'] = prev_value
            weapon_list.append(empty_dict.copy())
        for search_item in search_list:
            if (tmp_dict['D'] in search_item) and (tmp_dict['M'] in search_item):
                weapon_list.append(tmp_dict)

    # print(f'weapon_list = {weapon_list}')

    """ Преобразование библиотеки в список библиотек по типу оружия """
    tmp_list = []
    prev_value = weapon_list[0]['T']
    for value_dict in weapon_list:
        if value_dict['T'] == prev_value:
            tmp_list.append(value_dict)
        else:
            weapon_type_list.append(tmp_list.copy())
            prev_value = value_dict['T']
            tmp_list.clear()
            tmp_list.append(value_dict)
    weapon_type_list.append(tmp_list.copy())
    return weapon_type_list


if __name__ == '__main__':
    weapon_type_list = main(search_list)
    # print(f'weapon_type_list_final = {weapon_type_list}\n\n')

