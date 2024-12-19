import xlrd
from typing import Dict, List, Any


def main(search_list: List[Any]) -> List[List[Dict]]:
    """ Функция:
     1. получает список искомого оружия,
     2. считывает Excel файл с характеристиками всего имеющегося оружия,
     3. создает список искомого оружия, добавив к нему характеристики из Excel файла
     """

    template_list1 = ['Type', 'Class', 'Designation', 'Modification', 'Tonnage', 'Shots', 'DMG_Single', 'Heat',
                     'Ammo_Rounds', 'DMG_Full', 'DMG/Tonn', 'Heatsinks', 'Ammo_Tonns', 'Full_Weight']
    template_list = ['T', 'C', 'D', 'M', 'W', 'S', 'DS', 'H', 'AR', 'DF', 'DT', 'HS', 'AT', 'FW']
    empty_dict = {'T': ' ', 'C': ' ', 'D': ' ', 'M': ' ', 'W': 0, 'S': 0, 'DS': 0, 'H': 0, 'AR': 0,
                  'DF': 0, 'DT': 0, 'HS': 0, 'AT': 0, 'FW': 0}

    # Получение списка из Excel
    workbook = xlrd.open_workbook("BattleTech_Weapon_Efficiency.xls")
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

    energy_boost = search_list[-3][0]  # наличие усиления для Энергетического оружия
    ballistic_boost = search_list[-3][1]  # наличие усиления для Баллистического оружия
    boosty = ''
    if energy_boost:
        boosty = 'Energy'
    if ballistic_boost:
        boosty = 'Ballistic'

    # Преобразование списка из Excel в библиотеку
    weapon_list = []
    prev_value = ''
    search_list = search_list[1:-3]  # отсечение сервисной информации (прыжк. двиг., усиление, собств. охлаждение, вес)
    for item in income_list:  # для каждого элемента списка из Excel
        tmp_dict = dict(zip(template_list, item))  # создаем словарь по шаблону
        if tmp_dict['T'] == boosty:  # если есть усиливаемое оружие
            tmp_dict['DF'] *= 1.2
        if tmp_dict['T'] != prev_value:  # если данный тип вооружения еще не встречался
            prev_value = tmp_dict['T']
            empty_dict['T'] = prev_value  # создать словарь с этим типом вооружения и нулевыми параметрами
            weapon_list.append(empty_dict.copy())  # добавить этот "пустой" словарь в список оружия
        for search_item in search_list:  # для каждого элемента поискового списка
            if (tmp_dict['D'] in search_item) and (tmp_dict['M'] in search_item):  # если они же есть в текущем словаре
                weapon_list.append(tmp_dict)  # добавить этот словарь в список оружия

    # Преобразование библиотеки в список библиотек по типу оружия
    tmp_list = []
    weapon_type_list = []  # итоговый список типов оружия
    prev_value = weapon_list[0]['T']
    for value_dict in weapon_list:  # для каждого словаря в списке оружия
        if value_dict['T'] == prev_value:  # если тип оружия такой же, как и в предыдущем словаре
            tmp_list.append(value_dict)  # добавить словарь во временный список
        else:  # иначе
            weapon_type_list.append(tmp_list.copy())  # добавить временный словарь в список типов оружия
            prev_value = value_dict['T']
            tmp_list.clear()  # очистить временный список
            tmp_list.append(value_dict)  # добавить словарь во временный список
    weapon_type_list.append(tmp_list.copy())  # добавить последний временный словарь в список типов оружия
    return weapon_type_list


if __name__ == '__main__':
    weapon_type_list = main(search_list)
    # print(f'weapon_type_list_final = {weapon_type_list}\n\n')
