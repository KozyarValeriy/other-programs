import math

def S(D):
    ''' Function to calculate the square '''
    return math.pi * D*D / 4

def weight(L, D, Ro):
    ''' Function to calculate the weight '''
    return S(D) * L * Ro

def lt(a, b):
    return a < b

def count_weight(A, B, Ro):
    ''' Function to calculate the sum of the weight of all steps '''
    res = 0
    for i in range(len(A)):
        res += weight(A[i], B[i], Ro)
    return res

def find_lenth(D, M, Ro, D_list, L_list, L=40, eps=0.0005):
    ''' Function to search the size for specified weight '''
    M_cur = count_weight(L_list, D_list, Ro) + weight(L, D, Ro)
    first = lt(M_cur, M)
    delta = (1 if first else -1)
    while abs(M_cur - M) > eps:
        if first == lt(M_cur, M):
            L += delta
        else:
            L -= delta
            delta /= 10
        M_cur = count_weight(L_list, D_list, Ro) + weight(L, D, Ro)
    return L

if __name__ == '__main__':
    #lenth_mid = find_lenth(18.5, L3=50)
    # Parameters for calculating
    RO = 7800 # density kg/m^3
    RO = RO / (1000**2) # density g/cm^3
    D_first = [0.9, 0.9, 4.1, 4.1, 6, 6] # diameters of the steps
    L_first = [2.8, 2.5, 5, 5, 8, 8] # length of the steps
    M = 95 # required mass
    print('|{0: ^6s}|{1: ^8s}|{2: ^7s}|'.format('D', 'L', 'L_sum'))
    print('|{0:-^6s}|{1:-^8s}|{2:-^7s}|'.format('', '', ''))
    d = 18
    while d <= 19:
        lenth_mid = find_lenth(d, M, RO, D_first, L_first, L=50)
        print('|{0: ^6.1f}|{1: ^8.3f}|{2: ^7.2f}|'.format(d, lenth_mid, sum(L_first) + lenth_mid))
        d += 0.1
