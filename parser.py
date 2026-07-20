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

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"


TRACE_ON = True


def color(color):
    RESET = "\033[0m"

    def decorate(func):
        if not TRACE_ON:
            return func
        name = func.__name__

        def wrapper(*args, **kwargs):
            self = args[0]
            print(f"{color}{name}{RESET} {self.token = }")
            res = func(*args, **kwargs)
            print(f"{color}{name}{RESET} {self.token = }")

            return res

        return wrapper

    return decorate


class Parser:
    def __init__(self):
        self.tokens: Iterator[T.Token] = iter(())
        self.token: T.Token | None = None

    def _one_of(self, *sym) -> T.Token | None:
        if self.token in sym:
            return self.token
        return None

    @color(RED)
    def expr(self) -> N.Node:
        res = self.term()
        # while (op := self.token) and op in (T.Sym.PLUS, T.Sym.MINUS):
        while op := self._one_of(T.Sym.PLUS, T.Sym.MINUS):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    @color(RED)
    def term(self) -> N.Node:
        res = self.factor()
        while (op := self.token) and op in (T.Sym.MUL, T.Sym.DIV):
            self._consume()
            right = self.factor()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    @color(RED)
    def factor(self) -> N.Node:
        if self.token == LPAREN:
            self._consume()
            res = self.expr()
            self._expect(RPAREN)
        else:
            res = N.Num(self.token)
        self._advance()
        return res

    @color(GREEN)
    def _next(self, iter) -> T.Token | None:
        tok = next(self.tokens)
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
