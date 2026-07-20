#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, Any, get_args, get_origin, get_type_hints, Union
from enum import Enum
import inspect
import re


TOKEN_SPECS = {
    name: rf"(?P<{name}>{pat})"
    for name, pat in {
        "PLUS": r"\+",
        "MINUS": r"-",
        "MUL": r"\*",
        "DIV": r"/",
        "LPAREN": r"\(",
        "RPAREN": r"\)",
        "NAME": r"[A-Za-z_]\w*",
        "NUM": r"\d+",
        "WS": r"\s+",
    }.items()
}
Sym = Enum("Sym", TOKEN_SPECS)


def check_type(value: Any, hint: Any) -> bool:
    origin = get_origin(hint)
    if origin is Union:
        return any(check_type(value, h) for h in get_args(hint))
    if hint is Any:
        return True
    return isinstance(value, hint)


class TypedMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        super_init = clsdict["__init__"]

        sig = inspect.signature(super_init)
        hints = get_type_hints(super_init)

        def new_init(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, value in bound.arguments.items():
                if name not in hints:
                    continue

                hint = hints[name]
                assert check_type(value, hint), (
                    f"{name}={value!r} "
                    f"is {type(value).__name__}, "
                    f"expected {hint!r}"
                )

            return super_init(*args, **kwargs)

        clsdict["__init__"] = new_init
        return super().__new__(mcls, clsname, bases, clsdict)


class Token(metaclass=TypedMeta):
    def __init__(self, sym: Sym, val: float | str = ""):
        self.sym = sym
        self.val = val

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.sym == other.sym and self.val == other.val
        elif isinstance(other, Sym):
            print(type(self.sym), type(other))
            return self.sym.name == other.name
        else:
            return NotImplemented

    def __repr__(self):
        a = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({a})"


def iter_tokes(sexpr: str) -> Iterator[Token]:
    master_pat = "|".join(pat for _, pat in TOKEN_SPECS.items())
    for m in re.finditer(master_pat, sexpr):
        if m.lastgroup == Sym.WS.name:
            continue
        # yield Token(m.lastgroup, val=m.group(0))
        yield Token(Sym[m.lastgroup], val=m.group(0))


if __name__ == "__main__":
    for tok in iter_tokes("2 + (3 * 4) + 5"):
        print(tok)
