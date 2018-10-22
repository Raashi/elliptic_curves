import os
import sys

import generation
from ecurve import EllipticCurve, ECPoint

NAME_PROTOCOL = os.path.basename(sys.argv[0])[:-3]
FULL_NAME_PROTOCOL = 'files_' + NAME_PROTOCOL
if not os.path.exists(FULL_NAME_PROTOCOL):
    os.mkdir(FULL_NAME_PROTOCOL)


def read(filename):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename)) as f:
        return int(f.read())


def read_mul(*filenames):
    return (read(arg) for arg in filenames)


def read_struct(filename):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename)) as f:
        return eval(f.read())


def read_point(filename):
    p_xy, ec_ap = read_struct(filename)
    return ECPoint(*p_xy, EllipticCurve(*ec_ap))


def write(filename, value):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename), 'w') as f:
        f.write(str(value))


def write_point(filename, p: ECPoint):
    write(filename, (p.coords, (p.ec.a, p.ec.p)))


def delete(filename):
    if os.path.exists(os.path.join(FULL_NAME_PROTOCOL, filename)):
        os.remove(os.path.join(FULL_NAME_PROTOCOL, filename))


def exists(filename):
    return os.path.exists(os.path.join(FULL_NAME_PROTOCOL, filename))


def gen_curve(size):
    p, n, r, ec, g = generation.gen_curve(size)
    write('r.txt', r)
    write_point('G.txt', g)


def get_e(r, m, hash_function):
    with open(m, 'rb') as f:
        m = f.read()
    h = hash_function(m).digest()
    return int.from_bytes(h, byteorder='big') % r


def get_e_point(r, r_point, m, hash_function):
    with open(m, 'rb') as f:
        m = f.read()
    h = hash_function(m
                      + r_point.x.to_bytes(r_point.x.bit_length(), byteorder='big')
                      + r_point.y.to_bytes(r_point.y.bit_length(), byteorder='big')).digest()
    return int.from_bytes(h, byteorder='big') % r
