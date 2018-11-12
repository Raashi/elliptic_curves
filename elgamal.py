import random
import hashlib

from ecurve import EllipticCurve

from utils import ratio
from putils import *

hash_function = hashlib.sha256


def gen_keys(g, r):
    c = random.randint(1, r - 1)
    a = g * c
    write('c.txt', c)
    write_point('a.txt', a)


def sign(g, r, c, m):
    x, k, rp = 0, None, None
    while x == 0:
        k = random.randint(1, r - 1)
        rp = g * k
        x = rp.x
    e = get_e(r, m, hash_function)
    s = ratio(e + rp.x * c, k, r)

    write_point('rp.txt', rp)
    write('s.txt', s)


def check(r, g, a, rp, s, m, ec):
    if s < 1 or r < s or not rp.check_ec() or rp.ec != ec:
        print('Подпись недействительна')
        return
    es = get_e(r, m, hash_function)
    v1 = rp * s
    v2 = (g * es) + (a * rp.x)
    if v1 == v2:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')


def cleanup():
    delete('rp.txt')
    delete('s.txt')


def main():
    operation = sys.argv[1]
    if operation == '-gc':
        cleanup(), delete('c.txt'), delete('a.txt')
        gen_curve(int(sys.argv[2]))
    elif operation == '-gk':
        cleanup()
        gen_keys(read_point('g.txt'), read('r.txt'))
    elif operation == '-s':
        sign(read_point('g.txt'), read('r.txt'), read('c.txt'), sys.argv[2])
    elif operation == '-c':
        ec = EllipticCurve(read('ea.txt'), read('ep.txt'))
        check(read('r.txt'), read_point('g.txt'), read_point('a.txt'), read_point('rp.txt'), read('s.txt'), sys.argv[2], ec)


if __name__ == '__main__':
    main()
