#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import get_type_hints
from functools import wraps
from inspect import signature
from collections import defaultdict


def validate_init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        hints = get_type_hints(func)
        for name, hint in hints.items():
            if name == "self":
                continue
            # assert isinstance(bound.arguments[name], hint)
            if not isinstance(bound.arguments[name], hint):
                raise TypeError(f"{name!r} must be of type {hint.__name__!r}")
        return func(*args, **kwargs)

    return wrapper


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        mcls = type(cls)
        if cls not in mcls._instances:
            mcls._instances[cls] = super().__call__(*args, **kwargs)
        return mcls._instances[cls]


class CacheMeta(type):
    _cache = defaultdict(defaultdict())

    def __call__(cls, *args, **kwargs):
        mcls = type(cls)
        key = (args, tuple(sorted(kwargs.items())))
        if (cls not in mcls._cache) or (key not in mcls._cache[cls]):
            mcls._cache[cls][key] = super().__call__(*args, **kwargs)
        return mcls[cls][key]


class Logger(SingletonMeta):
    def __init__(self):
        print("Initializing Logger")


class Module(SingletonMeta):
    def __init__(self):
        print("Initializing Module")


class Person(CacheMeta):
    @validate_init
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    def __repr__(self):
        return f"Person({self.name}, {self.age}, {self.salary})"


if __name__ == "__main__":
    o1 = Logger()
    o2 = Logger()
    assert o1 is o2
    m1 = Module()
    m2 = Module()
    assert m1 is m2
    bob = Person("Bob", 37, 12000.0)
    max = Person("Max", 42, 24000.50)
    bob = Person("Bob", 37, 12000.0)
    bob = Person("Bob", 38, 12000.0)
