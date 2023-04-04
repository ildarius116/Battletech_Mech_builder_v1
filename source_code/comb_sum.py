import math

import excel_reader  # Модуль считывания данных об оружии из Excel файла


def combinations_with_replacement(iterable, r):
    """ Функция создания комбинаций оружия
        слегка переделанная из itertools.combinations_with_replacement
        combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    """
    pool = tuple(iterable)
    n = len(pool)
    r = int(r)
    if not n and r:
        return
    indices = [0] * r
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield list(pool[i] for i in indices)


def type_combo(search_list, weapon_type_list):
    """ Функция комбинации оружия внутри типа оружия
        выдает 4 комбинации (списком) каждого вида оружия по типу
        combinated_list = [
        [[{'T': 'Ballistic'}, {'T': 'Ballistic'}], [{'T': 'Ballistic'}, {'T': 'Ballistic'}]],
        [[{'T': 'Missile'}, {'T': 'Missile'}], [{'T': 'Missile'}, {'T': 'Missile'}]],
        [[{'T': 'Energy'}, {'T': 'Energy'}], [{'T': 'Energy'}, {'T': 'Energy'}], [{'T': 'Energy'}, {'T': 'Energy'}]],
        [[{'T': 'Support'}, {'T': 'Support'}], [{'T': 'Support'}, {'T': 'Support'}]]
        ]
     """

    combinated_list = []
    search_list = search_list[1:]
    for i, items in enumerate(weapon_type_list):
        combo = list(combinations_with_replacement(items, search_list[i][-1]))
        combinated_list.append(combo)
    # for i in combinated_list:
    #     print(f'combinated_list = {i}')
    return combinated_list


def product(*args):
    """ Функция создания комбинаций комбинаций типов оружия
        слегка переделанная из itertools.product
        product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
     """
    pools = (pool for pool in args)
    print()
    result = [[]]
    for pool in pools:
        result = [x+y for x in result for y in pool]
    return result


def final_combo(search_list, weapon_type_list):
    """ Функция комбинации комбинаций оружия перемешивает все 4 типа оружия (их списки комбинаций) между собой
    в общем виде:
     ['UAC/2', 'UAC/2', 'UAC/2', ' ', 'LRM10', 'LRM10', 'LRM10', 'M Laser', 'M Laser',
     'S Laser', 'S Laser', 'S Laser', 'S Laser', 'S Laser']
     """

    combinated_list = type_combo(search_list, weapon_type_list)
    final_combo_list = []
    for item in combinated_list:
        if final_combo_list:
            tmp_list = list(product(final_combo_list, item))
            final_combo_list = tmp_list.copy()
        else:
            final_combo_list = item
    return final_combo_list


def weight(search_list):
    """ Функция расчета доступного свободного веса
        Возвращает итоговый свободный вес, количество дополнительных или "не использованных" радиаторов
        и дельта температуры, при использовании прыжков
     """

    jumps_dict = {'Light': 0.5, 'Heavy': 1, 'Sturm': 2}
    initial_heat = 30  # собственное охлаждение пустого меха
    unused_initial_weight = 10  # "условный" вес 10ти "не использованных" радиаторов
    delta_jump_heat = 0
    income_weight = search_list[-1]  # свободный вес, указанный при расчете
    print('search_list[0] = ', search_list[0])

    if 'Jump Jets' in search_list[0]:
        quantity = int(search_list[0][2])   # кол-во прыжковых двигателей
        jump_weight = jumps_dict[search_list[0][1]] * quantity   # суммарный вес прыжковых двигателей
        jump_heat = quantity * 8   # суммарный нагрев от прыжка
        delta_jump_heat = jump_heat - initial_heat   # дельта охлаждения во время прыжка
        if delta_jump_heat >= 0:
            result_heatsink_weight = math.ceil(delta_jump_heat // 3)   # вес доп-ных радиаторов компенсации дельты
            free_weight = income_weight - jump_weight - result_heatsink_weight  # итоговый свободный вес
            delta_jump_heat -= result_heatsink_weight * 3  # итоговая дельта охлаждения во время прыжка
            unused_initial_weight = 0  # задействован весь "потенциал" собственного охлаждения меха
        else:
            result_heatsink_weight = math.floor(delta_jump_heat // 3)   # вес "не использованных" радиаторов дельты
            free_weight = income_weight - jump_weight  # итоговый свободный вес с учетом только двигателей
            delta_jump_heat -= result_heatsink_weight * 3  # итоговая дельта охлаждения во время прыжка
            unused_initial_weight += result_heatsink_weight  # "потенциал" охлаждения меха задействован частично
    else:
        result_heatsink_weight = -math.floor(initial_heat // 3)  # кол-во "не использованных" радиаторов дельты
        free_weight = income_weight   # итоговый свободный вес
    print('income_weight = ', income_weight)
    print('free_weight = ', free_weight)
    print('result_heatsink_weight = ', result_heatsink_weight)
    print('unused_initial_weight = ', unused_initial_weight)
    print('delta_jump_heat = ', delta_jump_heat)
    return free_weight, unused_initial_weight, result_heatsink_weight, delta_jump_heat


def best_combo(search_list):
    weapon_list = excel_reader.main(search_list)  # считывание списка вооружений из модуля excel_reader
    free_weight, unused_weight, add_heatsink, delta_jump_heat = weight(search_list)
    final_combo_list = final_combo(search_list, weapon_list)  # перебор комбинаций оружия
    max_dmg = 0
    for item_i in final_combo_list:  # в каждой комбинации комбинаций
        tmp_heat = []
        tmp_weight = []
        tmp_weapon = []
        tmp_dmg = []
        tmp_heatsink = []
        tmp_ammo = []
        for item_j in item_i:  # в каждой комбинации
            tmp_weapon.append(item_j['D'])  # список каждого оружия
            tmp_heat.append(item_j['H'])  # список нагрева каждого оружия
            tmp_weight.append(item_j['FW'])  # список веса каждого оружия
            tmp_dmg.append(item_j['DF'])  # список урона каждого оружия
            tmp_heatsink.append(item_j['HS'])  # список количества радиаторов для каждого оружия
            if isinstance(item_j['AT'], str):  # если боекомплект у оружия отсуствует
                tmp_ammo.append(0)  # боекомплект для каждого оружия устанавливается в НОЛЬ (цифра)
            else:
                tmp_ammo.append(item_j['AT'])  # список количества боекомплекта для каждого оружия
        curent_weight = sum(tmp_weight)  # суммарный вес оружия текущего списка веса каждого оружия
        cur_heatsink = sum(tmp_heatsink)  # суммарный вес радиаторов текущего списка веса каждого оружия
        if cur_heatsink >= unused_weight:  # если вес радиаторов комбинации >= незадействованного "потенциала"
            curent_weight -= unused_weight  # уменьшить текущий вес меньше на значение незадействованного "потенциала"
            cur_heatsink -= unused_weight  # уменьшить вес радиаторов на значение незадействованного "потенциала"
        else:
            curent_weight -= cur_heatsink  # уменьшить текущий вес на вес радиаторов комбинации
            cur_heatsink = 0  # обнуление суммарного веса радиаторов текущего списка веса оружия
        if curent_weight <= free_weight:  # если текущий вес не превышает свободный вес
            sum_dmg = sum(tmp_dmg)
            if sum_dmg >= max_dmg:  # суммарный урон выше текущего максимального значения урона
                max_dmg = sum_dmg
                sum_heat = (sum(tmp_heat) - (sum(tmp_heatsink) * 3)) + delta_jump_heat
                best_combo = tmp_weapon.copy()
                sum_dmg = sum(tmp_dmg)
                sum_ammo = sum(tmp_ammo)
                if add_heatsink > 0:  # если есть дополнительные радиаторы от прыжков
                    sum_weight = curent_weight + add_heatsink
                    sum_heatsink = cur_heatsink + add_heatsink
                    unallocated_weight = free_weight - sum_weight + add_heatsink
                else:
                    sum_weight = curent_weight
                    sum_heatsink = cur_heatsink
                    unallocated_weight = free_weight - sum_weight
    result = {'Best weapons: ': best_combo, 'Max Damage: ': sum_dmg, 'Summary weight: ': sum_weight,
              'Heatsink weight: ': sum_heatsink, 'Ammunition weight: ': sum_ammo,
              'Unallocated weight: ': unallocated_weight, 'Delta heat: ': sum_heat}
    if max_dmg == 0:
        return None
    # print('result = ', result)
    return result

if __name__ == '__main__':
    best_combo(search_list)
