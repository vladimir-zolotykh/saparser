#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import tokens as T
import node as N

PLUS = T.Sym.PLUS
MINUS = T.Sym.MINUS
MUL = T.Sym.MUL
DIV = T.Sym.DIV
NUM = T.Sym.NUM
LPAREN = T.Sym.LPAREN
RPAREN = T.Sym.RPAREN

TRACE_ON = True


def _trace(func):
    if not TRACE_ON:
        return func
    name = func.__name__

    def wrapper(*args, **kwargs):
        self = args[0]
        print(f"<_trace> {name} {self.token = }")
        res = func(*args, **kwargs)
        print(f"<_trace> {name} -> {res}")
        return res

    return wrapper


class Parser:
    def __init__(self):
        self.tokens: Iterator[T.Token] = iter(())
        self.token: T.Token | None = None

    @_trace
    def expr(self) -> N.Node:
        res = self.term()
        while (op := self.token) and op in (T.Sym.PLUS, T.Sym.MINUS):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    @_trace
    def term(self) -> N.Node:
        res = self.factor()
        while (op := self.token) and op in (T.Sym.MUL, T.Sym.DIV):
            self._consume()
            right = self.factor()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    @_trace
    def factor(self) -> N.Node:
        if self.token == LPAREN:
            self._consume()
            res = self.expr()
            self._expect(RPAREN)
        else:
            res = N.Num(self.token)
        self._advance()
        return res

    def _next(self, iter) -> T.Token | None:
        tok = next(self.tokens)
        print(f"<_next> {tok = }")
        return tok

    def _advance(self) -> T.Token:
        try:
            self.token = self._next(self.tokens)
        except StopIteration:
            self.token = None
        return self.token

    def _expect(self, expected: T.Sym) -> None:
        if not self.token == expected:
            raise SyntaxError(f"Got {self.token}, expected = {expected}")

    def _consume(self) -> None:
        self.token = self._next(self.tokens)

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokes(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    # n: N.Node = Parser().parse("2 + (3 * 4) + 5")
    n: N.Node = Parser().parse("2 + 3")
    print(n)
