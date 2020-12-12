class IntMathMixin(object):
    def __add__(self, other):
        return type(self)(int.__add__(self, other))

    def __sub__(self, other):
        return type(self)(int.__sub__(self, other))

    def __mul__(self, other):
        return type(self)(int.__mul__(self, other))

    def __matmul__(self, other):
        return type(self)(int.__matmul__(self, other))

    def __truediv__(self, other):
        return type(self)(int.__truediv__(self, other))

    def __floordiv__(self, other):
        return type(self)(int.__floordiv__(self, other))

    def __mod__(self, other):
        return type(self)(int.__mod__(self, other))

    def __divmod__(self, other):
        return type(self)(int.__divmod__(self, other))

    def __lshift__(self, other):
        return type(self)(int.__lshift__(self, other))

    def __rshift__(self, other):
        return type(self)(int.__rshift__(self, other))

    def __and__(self, other):
        return type(self)(int.__and__(self, other))

    def __xor__(self, other):
        return type(self)(int.__xor__(self, other))

    def __or__(self, other):
        return type(self)(int.__or__(self, other))
