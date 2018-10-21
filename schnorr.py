import random
import hashlib

from putils import *

hash_function = hashlib.sha256


def gen_points(r, g):
    p = g * random.randint(1, r - 1)
    a = random.randint(1, r - 1)
    q = p * a
    write('a.txt', a)
    write_point('P.txt', p)
    write_point('Q.txt', q)


def sign_r(r, p):
    k = random.randint(1, r - 1)
    r_point = p * k
    write('k.txt', k)
    write_point('Rp.txt', r_point)


def sign_e(r, r_point, m):
    write('e.txt', get_e_point(r, r_point, m, hash_function))


def sign(r, a, k, e):
    s = (k + a * e) % r
    write('s.txt', s)


def check_e(r, r_point, m):
    write('es.txt', get_e_point(r, r_point, m, hash_function))


def check(es, s, p, q, r_point):
    if r_point + (q * es) == p * s:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')


def main():
    operation = sys.argv[1]
    if operation == '-gc':
        gen_curve(int(sys.argv[2]))
    elif operation == '-gp':
        gen_points(read('r.txt'), read_point('G.txt'))
    elif operation == '-sr':
        sign_r(read('r.txt'), read_point('P.txt'))
    elif operation == '-se':
        sign_e(read('r.txt'), read_point('Rp.txt'), sys.argv[2])
    elif operation == '-s':
        sign(*read_mul('r.txt', 'a.txt', 'k.txt', 'e.txt'))
    elif operation == '-ce':
        check_e(read('r.txt'), read_point('Rp.txt'), sys.argv[2])
    elif operation == '-c':
        check(read('es.txt'), read('s.txt'), read_point('P.txt'), read_point('Q.txt'), read_point('Rp.txt'))
    elif operation == '-all':
        size = 10
        m = 'test.flac'
        modulo, n, r, ec, g = gen_curve(size)
        p = g * random.randint(1, r - 1)
        a = random.randint(1, r - 1)
        q = p * a
        k = random.randint(1, r - 1)
        r_point = p * k
        e = get_e(r, r_point, m)
        s = (k + a * e) % r
        print(r_point + (q * e) == p * s)


if __name__ == '__main__':
    main()
