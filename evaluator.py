#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from types import MethodType
from inspect import signature, _empty
from node import Node, Num, Plus, Minus, Mul, Div
from parser import Parser


class Method:
    def __init__(self, name):
        self._name = name
        self.methods = {}

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def register(self, func):
        sig = signature(func)
        typ = tuple()
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.annotation is _empty:
                raise TypeError(f"{name}: all params must be annotated")
            typ = typ + (parm.annotation,)
        self.methods[typ] = func

    def __call__(self, *args, **kwargs):
        typ = tuple(type(a) for a in args[1:])
        return self.methods[typ](*args)


class Dict(dict):
    def __setitem__(self, key, val):
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, val)
            return
        if key not in self:
            super().__setitem__(key, val)
        else:
            oval = self[key]
            if isinstance(oval, Method):
                mm = oval
                mm.register(val)
            else:
                mm = Method(key)
                mm.register(oval)
                mm.register(val)
            super().__setitem__(key, mm)


class MultiMeta(type):
    @classmethod
    def __prepare__(name, bases, ns):
        return Dict()


class Evaluator(metaclass=MultiMeta):
    def eval(self, n: Num) -> float:
        return float(n.val)

    def eval(self, n: Plus) -> float:  # noqa: F811
        return self.eval(n.left) + self.eval(n.right)

    def eval(self, n: Minus) -> float:  # noqa: F811
        return self.eval(n.left) - self.eval(n.right)

    def eval(self, n: Mul) -> float:  # noqa: F811
        return self.eval(n.left) * self.eval(n.right)

    def eval(self, n: Div) -> float:  # noqa: F811
        return self.eval(n.left) / self.eval(n.right)


if __name__ == "__main__":
    # n: Node = Parser().parse("2 * 3")
    n: Node = Parser().parse("2 + (3 * 4) + 5")
    print(n)
    print(Evaluator().eval(n))
