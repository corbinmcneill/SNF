from smithnormalform import ed, pid


class Z(ed.ED):
    def __init__(self, content):
        if isinstance(content, int):
            self.a = content
        elif isinstance(content, str):
            try:
                self.a = int(content)
            except ValueError:
                raise pid.InvalidInitialContent
        elif isinstance(content, list):
            if len(content) != 1 or not isinstance(content[0], int):
                raise pid.InvalidInitialContent
            else:
                self.a = content[0]
        else:
            raise pid.InvalidInitialContent

    def __str__(self):
        return str(self.a)

    def __hash__(self):
        return hash(self.a)

    def __eq__(self, x):
        return self.a == x.a

    def __ne__(self, x):
        return self.a != x.a

    def __neg__(self):
        return Z(-self.a)

    def __add__(self, x):
        return Z(self.a + x.a)

    def __sub__(self, x):
        return Z(self.a - x.a)

    def __mul__(self, x):
        return Z(self.a * x.a)

    def get_q(self, x):
        return Z(self.a // x.a)

    def get_r(self, x):
        return Z(self.a % x.a)

    def norm(self):
        return self.a * self.a

    @staticmethod
    def getZero():
        return Z(0)

    @staticmethod
    def getOne():
        return Z(1)

    def isUnit(self):
        return (self.a == 1) or (self.a == -1)
