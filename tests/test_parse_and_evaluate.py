import pytest

from parser import Parser
from evaluator import Evaluator


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("2 + 3 * 4", 14.0),  # precedence
        ("(2 + 3) * 4", 20.0),  # parentheses
        ("8 - 6 / 2", 5.0),  # minus and division
        ("18 / 3 * 2", 12.0),  # left associativity
    ],
)
def test_parse_and_evaluate(expr, expected):
    node = Parser().parse(expr)
    assert Evaluator().eval(node) == expected
