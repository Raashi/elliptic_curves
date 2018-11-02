import sys
from ecurve import *


def sqrt(a, p):
    a %= p
    res = []
    for x in range(p):
        if (x * x) % p == a:
            res.append(x)
    return res


def all_points(ec: EllipticCurve):
    n = 0
    res = []
    for x in range(ec.p):
        y = sqrt(x ** 3 + ec.a * x + ec.b, ec.p)
        for yi in y:
            n += 1
            print('({}, {})'.format(x, yi))
            res.append(ECPoint(x, yi, ec))
    print('N =', n + 1)
    res.append(ECPoint.zero())
    return res


def kpoint(p: ECPoint):
    """все kP для 1 < k < 5"""
    q = p
    print('kP для 1 < k < 5 и P = {}'.format(p.coords))
    for k in range(3):
        p = p + q
        print('{}P = {}'.format(k + 2, p.coords))


def find_gen(points):
    print('Нахождение образующих')
    for p in points:
        q, size = p + p, 1
        while q != p:
            q = q + p
            size += 1
        print('Точка P = {} является образующей подгруппы порядка {}'.format(p.coords, size))


def main():
    a, b, p = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ec = EllipticCurve(a, p, b)
    points = all_points(ec)
    kpoint(points[len(points) % 5])
    find_gen(points)
    p = ECPoint(4, 7, ec)
    print((p * 5).coords)


if __name__ == '__main__':
    main()
