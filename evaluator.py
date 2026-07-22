#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from types import MethodType
from inspect import signature
from node import Node, Num, Plus, Minus, Mul, Div
from parser import Parser


class Method:
    def __init__(self, *func):
        self.methods = {}
        self.register(*func)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def register(self, *func):
        def _register(func):
            typ = tuple(p.annotation for p in signature(func).parameters.values())[1:]
            self.methods[typ] = func

        for f in func:
            _register(f)

    def __call__(self, *args, **kwargs):
        typ = tuple(type(a) for a in args[1:])
        return self.methods[typ](*args)


class Dict(dict):
    def __setitem__(self, key, val):
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, val)
            return
        mm = self.get(key, Method())
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
    n: Node = Parser().parse("2 + (3 * 4) + 5")
    print(Evaluator().eval(n))
