import utils


def eq_points(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]


def eq_points_2(p1, p2, p):
    return p1[0] == p2[0] and p1[1] != p2[1] and pow(p1[1], 2, p) == pow(p2[1], 2, p)


def is_zero(point):
    return point[0] is None and point[1] is None


def add_points(p1, p2, a, p):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]

    if is_zero(p1):
        return p2
    elif is_zero(p2):
        return p1
    if eq_points_2(p1, p2, p):
        return None, None
    if not eq_points(p1, p2):
        lam = ((y2 - y1) % p) * utils.get_inverse((x2 - x1) % p, p) % p
    else:
        lam = (3 * x1 ** 2 + a) * utils.get_inverse((2 * y1) % p, p) % p

    x3 = (lam ** 2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return x3, y3


def mul_point(point, k, a, p):
    point_g = point[:]
    point_q = (None, None)

    kbin = bin(k)[2:]
    m = len(kbin)
    for i in range(m):
        if kbin[m - i - 1] == '1':
            point_q = add_points(point_q, point_g, a, p)
        point_g = add_points(point_g, point_g, a, p)

    return point_q


if __name__ == '__main__':
    ppoint = (1, 2)
    aa = 3
    pp = 65129
    NN = 64826
    res = mul_point(ppoint, NN - 1, aa, pp)
    assert res == (3, 6)

    xx0 = 1
    yy0 = 2
    aa = 3
    NN = 64826
    pp = 65129
    assert mul_point((xx0, yy0), NN, aa, pp) == (0, 0)
