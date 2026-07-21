#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import get_type_hints
from functools import wraps
from inspect import signature


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


class Person:
    @validate_init
    def __init__(self, name: str, age: int, salary: float):
        self.name = name
        self.age = age
        self.salary = salary

    def __repr__(self):
        args = ", ".join(f"{name}={val!r}" for name, val in self.__dict__.items())
        return f"{type(self).__name__}({args})"


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
