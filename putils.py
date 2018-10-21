import os
import sys

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
