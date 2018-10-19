import utils


class EllipticCurve:
    def __init__(self, a, p):
        self.a = a
        self.p = p


class ECPoint:
    def __init__(self, x, y, ec: EllipticCurve or None):
        self.ec = ec
        self.x = x
        self.y = y
        self.coords = (self.x, self.y)

    def __eq__(self, other):
        assert isinstance(other, ECPoint)
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return ECPoint(self.x, -self.y % self.ec.p, self.ec)

    @staticmethod
    def zero():
        return ECPoint(None, None, None)

    def __add__(self, other):
        assert isinstance(other, ECPoint)

        x1, y1, x2, y2 = self.x, self.y, other.x, other.y

        if self == ECPoint.zero():
            return ECPoint(other.x, other.y, other.ec)
        elif other == ECPoint.zero():
            return ECPoint(self.x, self.y, self.ec)
        if self == -other:
            return ECPoint.zero()
        if self != other:
            lam = ((y2 - y1) % self.ec.p) * utils.get_inverse((x2 - x1) % self.ec.p, self.ec.p) % self.ec.p
        else:
            lam = (3 * x1 ** 2 + self.ec.a) * utils.get_inverse((2 * y1) % self.ec.p, self.ec.p) % self.ec.p

        x3 = (lam ** 2 - x1 - x2) % self.ec.p
        y3 = (lam * (x1 - x3) - y1) % self.ec.p

        return ECPoint(x3, y3, self.ec)

    def __mul__(self, k):
        assert isinstance(k, int)

        g = ECPoint(self.x, self.y, self.ec)
        q = ECPoint.zero()

        kbin = bin(k)[2:]
        m = len(kbin)
        for i in range(m):
            if kbin[m - i - 1] == '1':
                q = q + g
            g = g + g

        return q


if __name__ == '__main__':
    test_ec = EllipticCurve(3, 65129)
    test_p = ECPoint(1, 2, test_ec)
    test_k = 64826
    assert test_p * (test_k + 1) == test_p

    test_p = ECPoint(1, 2, test_ec)
    assert test_p * test_k == ECPoint.zero()
