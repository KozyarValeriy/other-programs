import time

def calculate_time(fun):
    def wrap(*arg, **dct):
        first = time.clock()
        n = fun(*arg, **dct)
        print('Fibonacci number is equal {0}, takes {1:.3f} seconds'.format(n, time.clock() - first))
    return wrap

def fib(n: int, d: dict = dict()) -> int:
    assert n >= 0, 'Parameter "n" must be great or equal zero'
    if n not in d:
        if n <= 1:
            d[n] = n
        else:
            d[n] = fib(n - 1, d) + fib(n - 2, d)
    return d[n]

def fib2(n: int) -> int:
    assert n >= 0, 'Parameter "n" must be great or equal zero'
    if n <= 1:
        return n
    return fib2(n - 1) + fib2(n - 2)

if __name__ == '__main__':
    for i in range(10, 31):
        first = time.clock()
        print('Fibonacci_1 {0}, takes {1:.3f} seconds'.format(fib(i),
                                            time.clock() - first))
        first = time.clock()
        print('Fibonacci_2 {0}, takes {1:.3f} seconds'.format(fib2(i),
                                            time.clock() - first))
