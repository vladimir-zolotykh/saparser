#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from enum import Enum


TOKEN_SPECS = {
    "NUM": r"[A-Za-z_]\w*",
    "PLUS": r"\+",
    "MINUS": "-",
    "MUL": r"\*",
    "DIV": r"/",
    "WS": r"\s+",
}

Sym = Enum("Sym", TOKEN_SPECS)


class Token:
    def __init__(self, name: Sym, pat: str, val: str | float):
        pass


tokens = {name: Token(Sym[name], pat, pat) for name, pat in TOKEN_SPECS.items()}
