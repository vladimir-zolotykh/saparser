#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
from enum import Enum
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
        "EOF": "EOF",
    }.items()
}
Sym = Enum("Sym", TOKEN_SPECS)


class Token:
    def __init__(self, name: str, val: float | str = ""):
        self.name = name
        self.val = val

    def __repr__(self):
        a = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({a})"


def iter_tokes(sexpr: str) -> Iterator[Token]:
    master_pat = "|".join(pat for _, pat in TOKEN_SPECS.items())
    for m in re.finditer(master_pat, sexpr):
        if m.lastgroup == Sym.WS.name:
            continue
        yield Token(m.lastgroup, val=m.group(0))


if __name__ == "__main__":
    for tok in iter_tokes("2 + (3 * 4) + 5"):
        print(tok)
