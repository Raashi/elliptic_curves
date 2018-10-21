import random
import hashlib

from utils import ratio
from putils import *

hash_function = hashlib.sha256


def gen_keys(g, r):
    c = random.randint(1, r - 1)
    a = g * c
    write('c.txt', c)
    write_point('a.txt', a)


def sign_kr(g, r):
    x, k, rp = 0, None, None
    while x == 0:
        k = random.randint(1, r - 1)
        rp = g * k
        x = rp.x
    write('k.txt', k)
    write_point('rp.txt', rp)


def sign_e(r, m):
    write('e.txt', get_e(r, m, hash_function))


def sign(r, c, k, e, rp):
    s = ratio(e + rp.x * c, k, r)
    write('s.txt', s)


def check_e(r, m):
    write('es.txt', get_e(r, m, hash_function))


def check(r, s, es, g, a, rp):
    if (not (1 <= s < r)) or (rp.y ** 2 % rp.ec.p != (rp.x ** 3 + rp.ec.a * rp.x) % rp.ec.p):
        print('Подпись недействительна')
        return
    v1 = rp * s
    v2 = (g * es) + (a * rp.x)
    if v1 == v2:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')


def main():
    operation = sys.argv[1]
    if operation == '-gc':
        gen_curve(int(sys.argv[2]))
    elif operation == '-gk':
        gen_keys(read_point('G.txt'), read('r.txt'))
    elif operation == '-skr':
        sign_kr(read_point('G.txt'), read('r.txt'))
    elif operation == '-se':
        sign_e(read('r.txt'), sys.argv[2])
    elif operation == '-s':
        sign(*read_mul('r.txt', 'c.txt', 'k.txt', 'e.txt'), read_point('rp.txt'))
    elif operation == '-ce':
        check_e(read('r.txt'), sys.argv[2])
    elif operation == '-c':
        check(*read_mul('r.txt', 's.txt', 'es.txt'), read_point('g.txt'), read_point('a.txt'), read_point('rp.txt'))


if __name__ == '__main__':
    main()
