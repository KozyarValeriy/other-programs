# Программа для поиска решения линейного уравнения,
# записанного в любой форме. Для поиска коэффициентов
# используются регулярные выражения.

import re

def equation(s):
    a = b = c = ans = None
    try:
        s = s.lower().rstrip()
        s = s.replace(' ', '')
        a = re.findall('([-+]?\d*)x', s)[0]
        a = float(a)
        # searching c
        if re.match('[-+]?\d+$', s[s.index('=') + 1:]):
            c = float(re.findall('[-+]?\d+', s[s.index('=') + 1:])[0])
        elif re.match('^[-+]?\d+', s[:s.index('=')]):
            c = float(re.findall('[-+]?\d+', s[:s.index('=')])[0])
        # searching b    
        if s.index('x') < s.index('='):
            b = float(re.findall('[-+]?\d+[=+-]', s[:s.index('=') + 1])[0][:-1])
        else:
            if s.index('x') + 1 == len(s):
                b = float(re.findall('[=]?([-+]?\d+)[^x]', s[s.index('='):])[0])
            else:
                b = float(re.findall('[-+]?\d+$', s[s.index('='):])[0])
        ans = (c - b) / a
    except IndexError:
        print('Invalid input')
        print('Needed: ax + b = c')
        print('Input:  {0}'.format(s))
    except ValueError:
        print('Variable search error')
    return a, b, c, ans
    
def print_ans(s, a, b, c, ans):
    if ans is not None:
        s = s.replace('=', ' = ')
        s = s.replace('+', ' + ')
        s = s.replace('-', ' - ')
        s = s.replace('  ', ' ')
        print('For equation {0}:\nx = {1:.3f}'.format(s, ans))
        print('a = {0:.3f}, b = {1:.3f}, c = {2:.3f}'.format(a, b, c))
    


if __name__ == '__main__':
    assert equation('2x+5=-88') == (2, 5, -88, -46.5), 'Error 1'
    assert equation('-2x-5=88') == (-2, -5, 88, -46.5), 'Error 2'
    assert equation('-88= 5 - 2x') == (-2, 5, -88, 46.5), 'Error 3'
    assert equation('5-2x=-88') == (-2, 5, -88, 46.5), 'Error 4'
    assert equation('55 = 2x + 6') == (2, 6, 55, 24.5), 'Error 5'
    assert equation('-88 = -2x+8') == (-2, 8, -88, 48), 'Error 6'
    s = input('Input the equation like ax + b = c: ')
    answer = equation(s)
    print_ans(s, *answer)
