import random
import operator
import functools

import utils


small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # длина - 33 бита
mul_small_primes = functools.reduce(operator.mul, small_primes)

miller_rabin_tests_count = 5

debug_primes = False
last_gcd_trials = 1
last_small_trials = 1


def check_len(q, desired_size):
    return len(bin(q)) - 2 == desired_size


def isprime(prime):
    """
    источник: Маховенко. "Теоретическая криптография", стр. 166, алгоритм 7.7.1
    :param prime: проверяемое на простоту число
    :return: True - p простое, False - p составное
    """
    if prime & 1 == 0:
        return False

    q = prime - 1
    m = 0
    while q & 1 == 0:
        m += 1
        q //= 2
    s = q

    r = 0
    while r < miller_rabin_tests_count:
        a = random.randint(2, prime - 2)
        while utils.gcd(a, prime) > 1:
            a = random.randint(2, prime - 2)
        b = pow(a, s, prime)
        if b == 1:
            continue
        elif b == prime - 1:
            r += 1
            continue

        for l in range(1, m):
            c = pow(a, s * pow(2, l), prime)
            if c == prime - 1:
                r += 1
                break
        else:
            return False
    return True


def gen_odd(size):
    q = random.randint(2 ** (size - 1), 2 ** size - 1)
    if q & 1 == 0:
        q += 1
    return q


def gen_relatively_prime(size):
    q = gen_odd(size)

    global last_gcd_trials

    while utils.gcd(q, mul_small_primes) > 1 or q % 4 != 3:
        q += 2
        last_gcd_trials += 1
        if not check_len(q, size):
            q = gen_odd(size)

    return q


def gen_big_prime(size):
    """
    источник: https://pdfs.semanticscholar.org/873c/de422f7bc7903bfbaa3ff3e5477be92aa64a.pdf
    авторы: Marc Joye, Pascal Paillier, Serge Vaudenay

        'Efficient Generation of Prime Numbers'
            3.2 Classical Generation Algorithms

    функция генерирует простое число длины l бит с единичным старшим двоичным разрядом
    :param size: количество бит
    :return: простое l-битное число
    """
    q = gen_relatively_prime(size)

    global last_gcd_trials
    trials = 1
    last_gcd_trials = 1

    while not isprime(q) or q % 4 != 1:
        q += mul_small_primes
        trials += 1
        if not check_len(q, size):
            q = gen_relatively_prime(size)

    if debug_primes:
        print('Cгенерировано. Проверок на простоту: {:>3}. Проверок НОД: {:>3}'.format(last_gcd_trials, trials))

    return q


def gen_small_prime(size):
    q = gen_odd(size)

    global last_small_trials
    last_small_trials = 1

    while not isprime(q) or q % 4 != 1:
        q += 2
        last_small_trials += 1
        if not check_len(q, size):
            q = gen_odd(size)

    if debug_primes:
        print('Сгенерировано. Проверок на простоту: {:>3}'.format(last_small_trials))

    return q


def gen_prime(size):
    if size < 150:
        return gen_small_prime(size)
    else:
        return gen_big_prime(size)


if __name__ == '__main__':
    import sympy
    debug_primes = True
    # for _idx in range(100):
    #     test_len = random.randint(400, 1000)
    #     prime = gen_prime(test_len)
    #     assert check_len(test_len, prime)  # and sympy.isprime(prime)

    p = gen_prime(200)
    assert sympy.isprime(p)
