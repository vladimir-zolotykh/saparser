#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import iter_tokens as T
import node as N

PLUS = T.Sym.PLUS
MINUS = T.Sym.MINUS
MUL = T.Sym.MUL
DIV = T.Sym.DIV
NUM = T.Sym.NUM
LPAREN = T.Sym.LPAREN
RPAREN = T.Sym.RPAREN


class Parser:
    def __init__(self):
        self.tokens: Iterator[T.Token] = iter([])
        self.token: T.Token = T.Token(T.Sym.EOF)

    def expr(self) -> N.Node:
        res = self.term()
        while (op := self.token) and op in (T.Sym.PLUS, T.Sym.MINUS):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    def term(self) -> N.Node:
        res = self.factor()
        while (op := self.token) and op in (T.Sym.MUL, T.Sym.DIV):
            self._consume()
            right = self.factor()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    def factor(self) -> N.Node:
        if self.token == LPAREN:
            self._consume()
            res = self.expr()
            self._expect(RPAREN)
        else:
            res = N.Num(self.token)
        return res

    def _advance(self) -> T.Token:
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.token = T.Token(T.Sym.EOF)
        return self.token

    def _expect(self, expected: T.Sym) -> None:
        if not self.token == expected:
            raise SyntaxError(f"Got {self.token}, expected = {expected}")

    def _consume(self) -> None:
        self.token = next(self.tokens)

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokes(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    n: N.Node = Parser().parse("2 + (3 * 4) + 5")
    print(n)
