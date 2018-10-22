import random

from putils import *


def get_check_rounds():
    if not exists('rounds.txt'):
        write('rounds.txt', 0)

    rounds = read('rounds.txt')
    if rounds < 0:
        print('ОШИБКА: Пегги обманывает. Обмен данными недопустим')
    return rounds


def cleanup():
    for entry in os.listdir(FULL_NAME_PROTOCOL):
        os.remove(os.path.join(FULL_NAME_PROTOCOL, entry))


def cleanup_round():
    delete('ra.txt'), delete('a.txt'), delete('bit.txt'), delete('parcel.txt')


def gen_x(g, r):
    x = random.randint(1, r - 1)
    b = g * x
    write('x.txt', x)
    write_point('b.txt', b)


def round_a(g, r):
    if get_check_rounds() < 0:
        return
    ra = random.randint(1, r - 1)
    a = g * ra
    write('ra.txt', ra)
    write_point('a.txt', a)


def round_bit(a, r):
    if get_check_rounds() < 0:
        return
    if a * r != ECPoint.zero() or a == ECPoint.zero():
        print('Пегги не знает x')
        write('rounds.txt', -1)
        cleanup_round()
        return
    b = random.getrandbits(1)
    write('bit.txt', b)


def round_parcel(bit, x, r, ra):
    if get_check_rounds() < 0:
        return
    if bit == 1:
        write('parcel.txt', ra)
    else:
        m = (x + ra) % r
        write('parcel.txt', m)


def check(g, parcel, a, b, bit):
    rounds = get_check_rounds()
    if rounds < 0:
        return

    if (bit == 1 and a == g * parcel) or (bit == 0 and g * parcel == a + b):
        rounds += 1
        print('Раунд пройден. Пегги обманывает с вероятностью 1/{}'.format(2 ** rounds))
        write('rounds.txt', rounds)
    else:
        print('Пегги не знает x')
        write('rounds.txt', -1)

    cleanup_round()


if __name__ == '__main__':
    operation = sys.argv[1]

    if operation == '-gp':
        cleanup()
        gen_curve(int(sys.argv[2]))
    elif operation == '-gx':
        cleanup_round(), delete('rounds.txt')
        gen_x(read_point('g.txt'), read('r.txt'))
    elif operation == '-ra':
        round_a(read_point('g.txt'), read('r.txt'))
    elif operation == '-rb':
        round_bit(read_point('a.txt'), read('r.txt'))
    elif operation == '-rp':
        round_parcel(*read_mul('bit.txt', 'x.txt', 'r.txt', 'ra.txt'))
    elif operation == '-c':
        check(read_point('g.txt'), read('parcel.txt'), read_point('a.txt'), read_point('b.txt'), read('bit.txt'))
    elif operation == '-round':
        _rounds = get_check_rounds()
        if _rounds < 0:
            sys.exit(1)
        _g, _r, _x, _b = read_point('g.txt'), read('r.txt'), read('x.txt'), read_point('b.txt')
        round_a(_g, _r)
        round_bit(read_point('a.txt'), _r)
        round_parcel(*read_mul('bit.txt', 'x.txt', 'r.txt', 'ra.txt'))
        check(_g, read('parcel.txt'), read_point('a.txt'), _b, read('bit.txt'))
    else:
        print('ОШИБКА: Неверная операция')
