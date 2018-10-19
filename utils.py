def gcd(x, y):
    x, y = max(x, y), min(x, y)
    while y:
        x, y = y, x % y
    return x


def gcdex(a, b):
    a, b = max(a, b), min(a, b)

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
    if a == 0:
        raise ArithmeticError('Обратного элемента не существует')
    if a == 1:
        return 1

    res = pow(a, m - 2, m)
    if (a * res) % m != 1:
        raise Exception('Неверно взят обратный элемент {} и {} = {}'.format(a, m, (a * res) % m))

    return res
