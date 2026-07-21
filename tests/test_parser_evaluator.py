import pytest

from parser import Parser
from evaluator import Evaluator


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("8 - 6 / 2", 5.0),
        ("18 / 3 * 2", 12.0),
        ("2 + (3 * 4) + 5", 19.0),
    ],
)
def test_evaluator(expr, expected):
    node = Parser().parse(expr)
    assert Evaluator().eval(node) == expected


def test_parser_respects_precedence():
    node = Parser().parse("2 + 3 * 4")
    assert Evaluator().eval(node) == 14.0


def test_parser_respects_parentheses():
    node = Parser().parse("(2 + 3) * 4")
    assert Evaluator().eval(node) == 20.0
