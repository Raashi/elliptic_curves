import random
import hashlib

from putils import *

hash_function = hashlib.sha256


def write_sign(p: ECPoint, s):
    write('sign.txt', (p.coords, (p.ec.a, p.ec.p), s))


def read_sign():
    dsign = read_struct('sign.txt')
    coords, e, s = dsign
    p = ECPoint(*coords, EllipticCurve(*e))
    return p, s


def gen_key(r, g):
    p = g * random.randint(1, r - 1)
    a = random.randint(1, r - 1)
    q = p * a
    write('a.txt', a)
    write_point('p.txt', p)
    write_point('q.txt', q)


def sign(r, p, a, m):
    k = random.randint(1, r - 1)
    rp = p * k
    e = get_e_point(r, rp, m, hash_function)
    s = (k + a * e) % r
    write_sign(rp, s)


def check(p, q, r, dsign, m):
    rp, s = dsign
    if rp.ec != EllipticCurve(read('ea.txt'), read('ep.txt')):
        print('Подпись недействительна')
        return
    es = get_e_point(r, rp, m, hash_function)
    if rp + (q * es) == p * s:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')


def main():
    operation = sys.argv[1]

    if operation == '-gc':
        # os.remove('sign.txt'), os.remove('p.txt'), os.remove('q.txt'), os.remove('a.txt')
        gen_curve(int(sys.argv[2]))
    elif operation == '-gp':
        # os.remove('sign.txt')
        gen_key(read('r.txt'), read_point('g.txt'))
    elif operation == '-s':
        sign(read('r.txt'), read_point('p.txt'), read('a.txt'), sys.argv[2])
    elif operation == '-c':
        check(read_point('p.txt'), read_point('q.txt'), read('r.txt'), read_sign(), sys.argv[2])
    else:
        print('Неверный код операции')


if __name__ == '__main__':
    main()
