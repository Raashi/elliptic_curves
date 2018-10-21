def gcd(x, y):
    x, y = max(x, y), min(x, y)
    while y:
        x, y = y, x % y
    return x


def egcd(a, b):
    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    q, r2 = r0 // r1, r0 % r1
    while r2 != 0:
        x1, x0 = x0 - q * x1, x1
        y1, y0 = y0 - q * y1, y1

        r1, r0 = r2, r1
        q, r2 = r0 // r1, r0 % r1

    return r1, x1, y1


def get_inverse(a, m):  # in ring
    a %= m
    if a == 0:
        return 0
    if gcd(a, m) != 1:
        raise ArithmeticError('gcd(a={}, m={}) не равен 1 для нахождения обратного'.format(a, m))
    d, x, y = egcd(a, m)
    assert d == 1 and (x * a) % m == 1
    return x % m


def ratio(p, q, m):  # in ring
    p, q = p % m, q % m
    return (p * get_inverse(q, m)) % m
