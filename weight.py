import math


def square_circle(diameter: int or float) -> float:
    """ Функция для расчета площади круга

    :param diameter: диаметр окрыжности в мм,
    :return: площадь круга в мм^2.
    """
    return math.pi * (diameter ** 2) / 4


def weight(length: int or float, diameter: int or float, ro_: int) -> float:
    """ Функция для массы цилиндра

    :param length: высота цилиндра в мм,
    :param diameter: диаметр круга в мм,
    :param ro_: плотность материала в кг/м^3,
    :return: площадь цилиндра в мм^2.
    """
    return square_circle(diameter) * length * ro_


def lt(a: int or float, b: int or float) -> bool:
    """ Функция less_then """
    return a < b


def summary_weight(length_list: list, diameter_list: list, ro_: int) -> float:
    """ Функция для расчета суммарной массы

    :param length_list: список длин каждого учатска цилиндра,
    :param diameter_list: список диаметров каждого участка цилиндра,
    :param ro_: плотность материала,
    :return: суммарная масса цилиндра.
    """
    res = 0
    for i in range(len(length_list)):
        res += weight(length_list[i], diameter_list[i], ro_)
    return res


def find_length(diameter, aim_mass, ro_, diameter_list, length_list, start_length=40, eps=0.0005):
    """ Function to search the size for specified weight """
    current_mass = summary_weight(length_list, diameter_list, ro_) + weight(start_length, diameter, ro_)
    first = lt(current_mass, aim_mass)
    delta = (1 if first else -1)
    while abs(current_mass - aim_mass) > eps:
        if first == lt(current_mass, aim_mass):
            start_length += delta
        else:
            start_length -= delta
            delta /= 10
        current_mass = summary_weight(length_list, diameter_list, ro_) + weight(start_length, diameter, ro_)
    return start_length


if __name__ == '__main__':
    # length_mid = find_length(18.5, L3=50)
    # Parameters for calculating
    ro = 7800  # density kg/m^3
    ro = ro / (1000 ** 2)  # density g/cm^3
    diameter_first = [0.9, 0.9, 4.1, 4.1, 6, 6]  # diameters of the steps
    length_first = [2.8, 2.5, 5, 5, 8, 8]  # length of the steps
    mass = 95  # required mass
    print('|{0: ^6s}|{1: ^8s}|{2: ^7s}|'.format('D', 'L', 'L_sum'))
    print('|{0:-^6s}|{1:-^8s}|{2:-^7s}|'.format('', '', ''))
    d = 18
    while d <= 19:
        length_mid = find_length(d, mass, ro, diameter_first, length_first, start_length=50)
        print('|{0: ^6.1f}|{1: ^8.3f}|{2: ^7.2f}|'.format(d, length_mid, sum(length_first) + length_mid))
        d += 0.1
