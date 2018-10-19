import os
import sys

NAME_PROTOCOL = os.path.basename(sys.argv[0])[:-3]
FULL_NAME_PROTOCOL = 'files_' + NAME_PROTOCOL
if not os.path.exists(FULL_NAME_PROTOCOL):
    os.mkdir(FULL_NAME_PROTOCOL)


def read(filename):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename)) as f:
        return int(f.read())


def read_struct(filename):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename)) as f:
        return eval(f.read())


def read_mul(*filenames):
    return (read(arg) for arg in filenames)


def write(filename, value):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename), 'w') as f:
        f.write(str(value))


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
    if a == 0:
        return 0
    if gcd(a, m) != 1:
        raise ArithmeticError('gcd(a={}, m={}) не равен 1 для нахождения обратного'.format(a, m))
    d, x, y = egcd(a, m)
    assert d == 1 and (x * a) % m == 1
    return x % m
