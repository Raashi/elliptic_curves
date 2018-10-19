import random
import operator
import functools

import utils


SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # длина - 33 бита
SMALL_PRIMES_PRODUCT = functools.reduce(operator.mul, SMALL_PRIMES)
MR_TESTS = 5


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
    while r < MR_TESTS:
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
    while utils.gcd(q, SMALL_PRIMES_PRODUCT) > 1 or q % 4 != 3:
        q += 2
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
    while not isprime(q) or q % 4 != 1:
        q += SMALL_PRIMES_PRODUCT
        if not check_len(q, size):
            q = gen_relatively_prime(size)
    return q


def gen_small_prime(size):
    q = gen_odd(size)
    while not isprime(q) or q % 4 != 1:
        q += 2
        if not check_len(q, size):
            q = gen_odd(size)
    return q


def gen_prime(size):
    return gen_small_prime(size) if size < 150 else gen_big_prime(size)


if __name__ == '__main__':
    pass
