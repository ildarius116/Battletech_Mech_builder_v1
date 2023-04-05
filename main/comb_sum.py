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
    return combinated_list


def product(*args):
    """ Функция создания комбинаций комбинаций типов оружия
        слегка переделанная из itertools.product
        product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
     """

    pools = (pool for pool in args)
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
        Возвращает:
         итоговый свободный вес,
         собственное охлаждение (пустого) Меха,
         не использованный "потенциал" охлаждения Меха,
         количество дополнительных (положительное значение) или "не использованных" (отрицательное значение) радиаторов,
         дельта температуры, при использовании прыжков
     """

    jumps_dict = {'Standard': 0.5, 'Heavy': 1, 'Assault': 2}
    jump_heat = jump_weight = 0
    income_weight = search_list[-1]  # свободный вес, указанный при расчете
    initial_heat = search_list[-2]  # собственное охлаждение пустого меха
    quantity = int(search_list[0][-1])  # кол-во прыжковых двигателей
    if quantity and search_list[0][0] == 'Jump Jets':
        jump_weight = jumps_dict[search_list[0][1]] * quantity   # суммарный вес прыжковых двигателей
        jump_heat = quantity * 2   # суммарный нагрев от прыжка
        delta_jump_heat = initial_heat - jump_heat  # дельта охлаждения во время прыжка
        free_weight = income_weight - jump_weight  # свободный вес с учетом двигателей и прыжков
        unused_initial_weight = delta_jump_heat // 3   # вес "не использованных" радиаторов дельты охлаждения
    else:
        unused_initial_weight = math.floor(initial_heat // 3)  # "условный" вес 10/20ти "не использованных" радиаторов
        free_weight = income_weight   # итоговый свободный вес
    return free_weight, initial_heat, unused_initial_weight, jump_weight, jump_heat


def best_combo(search_list):
    """ Функция поиска лучшей (с максимальным уроном) комбинации оружия """

    max_dmg = 0
    free_weight, initial_heat, unused_weight, jump_weight, jump_heat = weight(search_list)
    weapon_list = excel_reader.main(search_list)  # считывание списка вооружений из модуля excel_reader
    final_combo_list = final_combo(search_list, weapon_list)  # перебор комбинаций оружия

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
            if isinstance(item_j['AT'], str):  # если боекомплект у оружия отсутствует
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
                result_heat = sum(tmp_heat) + jump_heat - cur_heatsink * 3 - initial_heat
                best_combo = tmp_weapon.copy()
                sum_ammo = sum(tmp_ammo)
                sum_weight = curent_weight
                sum_heatsink = cur_heatsink
                unallocated_weight = free_weight - sum_weight
                if unallocated_weight > 0 and result_heat > 2:  # если есть нераспределенный вес и нагрев больше 2
                    additional_heatsink = result_heat // 3  # сколько надо дополнительных радиаторов
                    if unallocated_weight >= additional_heatsink:  # если нераспределенный вес не меньше доп. радиаторов
                        unallocated_weight -= additional_heatsink
                        sum_heatsink += additional_heatsink
                        sum_weight += additional_heatsink
                        result_heat -= additional_heatsink * 3
                    else:
                        additional_heatsink -= unallocated_weight
                        sum_heatsink += unallocated_weight
                        sum_weight += unallocated_weight
                        result_heat -= unallocated_weight * 3
                        unallocated_weight = 0
    sum_weight += jump_weight
    result = {'Best weapons: ': best_combo, 'Max Damage: ': max_dmg, 'Summary weight: ': sum_weight,
              'Heatsink weight: ': sum_heatsink, 'Ammunition weight: ': sum_ammo,
              'Unallocated weight: ': unallocated_weight, 'Delta heat: ': result_heat}
    if max_dmg == 0:  # если ни одна комбинация не прошла по весу
        return None
    return result

if __name__ == '__main__':
    best_combo(search_list)
