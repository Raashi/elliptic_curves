import sys
import random

import utils
import prime
import factorization
import elliptic_curve as ecurve

import sympy
import matplotlib.pyplot as pyplot

m_table_log = [100, 150, 200, 250, 300, 350, 400]
m_table = {
    1:    [71, 141, 232, 342, 470, 617, 782],
    1.57: [21,  42,  67,  99, 136, 178, 225],
    1.92: [12,  24,  39,  58,  78, 103, 129]
}


def choose_m(size):
    c = 1.92
    if size in m_table_log:
        return m_table[c][m_table_log.index(size)]
    else:
        if size < m_table_log[0]:
            return m_table[c][0]
        elif size > m_table_log[-1]:
            return m_table[c][-1]
        else:
            for a, b in zip(m_table_log[:-1], m_table_log[1:]):
                if a < size < b:
                    return m_table[c][m_table_log.index(b)]


def gen_pNr(size, m):
    trials = 0
    while True:
        trials += 1
        # 1 шаг
        p = prime.gen_prime(size)
        assert p % 4 == 1
        assert sympy.isprime(p)

        # 2 шаг (страница 168, алгоритм 7.8.1)
        a, b = factorization.get_factors(p, 1)
        assert a * a + b * b == p

        # 3 шаг
        T = [2 * a, -2 * a, 2 * b, -2 * b]
        for t in T:
            N = p + 1 + t
            rs = [N // 2, N // 4]
            for r in rs:
                if prime.isprime(r):
                    assert sympy.isprime(r)
                    # шаг 4
                    if p != r:
                        for i in range(1, m + 1):
                            if pow(p, i, r) == 1:
                                break
                        else:
                            print('Попыток сгенерировать p, N, r = {}'.format(trials))
                            return p, N, r


def gen_point(p, N, r):
    trials = 1
    while True:
        x0 = random.randint(1, p - 1)
        y0 = random.randint(1, p - 1)
        A = ((y0 ** 2 - x0 ** 3) * utils.get_inverse(x0, p)) % p

        if (N == 2 * r and factorization.legendre_symbol((-A) % p, p) == -1) or \
                (N == 4 * r and factorization.legendre_symbol((-A) % p, p) == 1):
            point = ecurve.mul_point((x0, y0), N, A, p)
            if point == (None, None):
                print('Попыток сгенерировать Q =', trials)
                return x0, y0, A
        trials += 1


def draw_points(Q, r, a, p):
        pyplot.figure()
        point = (None, None)
        for k in range(0, r):
            pyplot.scatter(*point)
            point = ecurve.add_points(point, Q, a, p)
        pyplot.show()


def print_points(Q, r, a, p):
        point = (None, None)
        for k in range(0, r):
            point = ecurve.add_points(point, Q, a, p)
            print('{}-ая точка:'.format(k + 1), point)


def main():
    """
    источник: Маховенко. "Теоретическая криптография", стр. 304, алгоритм 15.3.2
    """
    arg_draw = '-d' in sys.argv
    arg_print = '-p' in sys.argv

    size = int(sys.argv[1])
    assert size > 4, 'Лучше выбирать длину числа-порядка поля > 4'
    m = choose_m(size)
    print('Выбрано m = {}'.format(m))

    p, N, r = gen_pNr(size, m)
    x0, y0, A = gen_point(p, N, r)
    Q = ecurve.mul_point((x0, y0), N // r, A, p)
    assert ecurve.mul_point(Q, r, A, p) == (None, None)  # проверяем, что порядок точки Q равен r

    print('Порядок p поля =', p)
    print('Параметр А ЭК =', A)
    print('Образующая точка Q =', Q)
    print('Порядок r циклической подгруппы точек =', r)

    if arg_print:
        print_points(Q, r, A, p)
    if arg_draw:
        draw_points(Q, r, A, p)


if __name__ == '__main__':
    main()
