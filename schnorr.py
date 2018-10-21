import random
import hashlib

from putils import *
import generation

hash_function = hashlib.sha256


def gen_curve(size):
    p, n, r, ec, g = generation.gen_curve(size)
    write('r.txt', r)
    write_point('G.txt', g)


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


def get_e(r, r_point, m):
    with open(m, 'rb') as f:
        m = f.read()
    h = hash_function(m
                      + r_point.x.to_bytes(r_point.x.bit_length(), byteorder='big')
                      + r_point.y.to_bytes(r_point.y.bit_length(), byteorder='big')).digest()
    return int.from_bytes(h, byteorder='big') % r


def sign_e(r, r_point, m):
    write('e.txt', get_e(r, r_point, m))


def sign(r, a, k, e):
    s = (k + a * e) % r
    write('s.txt', s)


def check_e(r, r_point, m):
    write('es.txt', get_e(r, r_point, m))


def check(es, s, p, q, r_point):
    if r_point + (q * es) == p * s:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')


def main():
    operation = sys.argv[1]
    if operation == '-gcurve':
        gen_curve(int(sys.argv[2]))
    elif operation == '-gpoints':
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
        modulo, n, r, ec, g = generation.gen_curve(size)
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
