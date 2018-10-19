import utils


def legendre_symbol(a, p):
    """
    источник: Маховенко Е.Б. 'Теоретическая криптография', стр. 83
    :return: значение символа Лежандра (1, -1, 0)
    """
    if a % p == 0:
        return 0
    if utils.gcd(a, p) != 1:
        raise Exception('Символ Лежандра имеет смысл для взаимно простых a и p')

    q = pow(a, (p - 1) // 2, p)
    if q == 1:
        return 1
    elif q == p - 1:
        return -1
    else:
        raise Exception('Неверно вычислен символ Лежандра')


def gen_b(p):
    b = 1
    while legendre_symbol(b, p) != -1:
        b += 1
    return b


def shenks_tonelli(p, n):
    n = n % p
    s = p - 1
    r = 0

    # получаем разложение p-1 = s*2**r
    while s % 2 == 0:
        s //= 2
        r += 1

    # начальные значения: λ и ω
    l = pow(n, s, p)
    w = pow(n, (s + 1) // 2, p)
    # находим порядок λ
    mod = l
    m = 0
    while mod != 1:
        mod = (mod * mod) % p
        m += 1

    # находим квадратичный невычет
    z = gen_b(p)
    # находим коэф-ты, на которые будем умножать
    yd_l = pow(pow(z, s, p), pow(2, r - m), p)
    yd_w = pow(pow(z, s, p), pow(2, r - m - 1), p)
    # находим корень
    while l != 1:
        l = (l * yd_l) % p
        w = (w * yd_w) % p

    return w


def get_factors(p, D):
    if legendre_symbol(p - D, p) == -1:
        return None, None

    u = shenks_tonelli(p, -D)
    assert (u * u) % p == (-D) % p

    u_i = [u]
    m_i = [p]

    while m_i[-1] != 1:
        m_i.append((u_i[-1] ** 2 + D) // m_i[-1])
        u_i.append(min(u_i[-1] % m_i[-1], (m_i[-1] - u_i[-1]) % m_i[-1]))
    m_i.pop()
    u_i.pop()

    a = u_i[-1]
    b = 1
    for idx in range(len(m_i) - 2, -1, -1):
        a, b = get_new_ab(a, b, u_i[idx], D)

    a %= p
    b %= p

    a = min(p - a, a)
    b = min(p - b, b)
    return a, b


def get_new_ab(ai, bi, u, D):
    ratio = ai ** 2 + D * bi ** 2

    a1 = u * ai + D * bi
    a2 = -u * ai + D * bi
    if a1 % ratio == 0:
        a = a1 // ratio
    elif a2 % ratio == 0:
        a = a2 // ratio
    else:
        raise Exception('Не могу посчитать a_i-1')

    b1 = -ai + u * bi
    b2 = -ai - u * bi

    if b1 % ratio == 0:
        b = b1 // ratio
    elif b2 % ratio == 0:
        b = b2 // ratio
    else:
        raise Exception('Не могу посчитать b_i-1')

    return a, b


if __name__ == '__main__':
    # import prime
    # import sympy
    # for _idx in range(10):
    #     pp = prime.gen_prime(100)
    #     while pp % 4 != 1:
    #         pp = prime.gen_prime(100)
    #     assert sympy.isprime(pp)
    #     aa, bb = get_factors(pp, 1)
    #     assert aa * aa + bb * bb == pp, 'пройдено тестов ' + str(_idx + 1)
    d = 65128
    p = 65129
    res = shenks_tonelli(p, d)
    assert pow(res, 2, p) == d
