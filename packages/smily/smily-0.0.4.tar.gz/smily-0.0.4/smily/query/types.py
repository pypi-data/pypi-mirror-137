import pandas as pd
from pytimeparse.timeparse import timeparse

from . import operator as op


class Base:
    def convert(self, value):
        return value

    def __iter__(self):
        yield op.has(self.name)

    def __invert__(self):
        return [op.hasnot(self.name)]


class Equals(Base):
    def __eq__(self, other):
        return [op.eq(self.name, self.convert(other))]


class NotEquals(Base):
    def __ne__(self, other):
        return [op.ne(self.name, self.convert(other))]


class Equality(Equals, NotEquals):
    pass


class GreaterThan(Base):
    def __gt__(self, other):
        return [op.gt(self.name, self.convert(other))]


class GreaterEquals(Base):
    def __ge__(self, other):
        return [op.ge(self.name, self.convert(other))]


class LessThan(Base):
    def __lt__(self, other):
        return [op.lt(self.name, self.convert(other))]


class LessEquals(Base):
    def __le__(self, other):
        return [op.le(self.name, self.convert(other))]


class Contains(Base):
    def contains(self, other):
        return [op.contains(self.name, self.convert(other))]


class In(Base):
    def one_of(self, args):
        return [op.in_(self.name, ",".join(args))]


class Ordered(Equals, NotEquals, GreaterThan, GreaterEquals, LessThan, LessEquals):
    pass


class Any(Ordered, Contains, In):
    pass


class DictField(Ordered):
    def __init__(self, name):
        self.name = name

    def __iter__(self):
        yield op.has(self.name)

    def __invert__(self):
        return [op.hasnot(self.name)]


class Dict:
    def __getattr__(self, name):
        return DictField(f"{self.name}.{name}")


class String(Equality, Contains, In):
    pass


class Number(Ordered):
    pass


class Duration(Number):
    def convert(self, value):
        val = timeparse(value)
        if val is not None:
            return str(val)

        return value


class Timestamp(Number):
    def convert(self, value):
        t = pd.Timestamp(value)
        if t.tzinfo:
            t = t.tz_convert("UTC")
        return t.strftime("%Y-%m-%dT%H:%M:%SZ")
