from decimal import Decimal, localcontext


def solution(s):
    n = Decimal(s)
    with localcontext() as ctx:
        ctx.prec = 102
        r = Decimal(2).sqrt()
        s = Decimal(2) + Decimal(2).sqrt()

        def solve(n):
            if n == 0:
                return 0
            Brn = int(r * n)
            Brns = int(Decimal(Brn) / s)

            return (Brn * (Brn + 1)) / 2 - solve(Brns) - Brns * (Brns + 1)

        return str(int(solve(n)))

