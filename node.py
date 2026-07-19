#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import iter_tokens as T


class Node:
    def __init__(self, val: float | T.Sym):
        self.val = val


class Num(Node):
    def __repr__(self):
        return f"{type(self).__name__}({self.val!r})"


class BinOp(Node):
    def __init__(self, left: Node, right: Node):
        super().__init__(self._op)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"


class Plus(BinOp):
    _op = T.Sym.PLUS


class Minus(BinOp):
    _op = T.Sym.MINUS


class MUL(BinOp):
    _op = T.Sym.MINUS


class DIV(BinOp):
    _op = T.Sym.MINUS
