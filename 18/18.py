from os.path import abspath, dirname, join
from typing import List, Tuple

from lark import Lark, Transformer, v_args
advent_of_code_left_to_right_grammar = """
    ?start: expression
    ?expression: atom
        | expression "+" atom   -> add
        | expression "*" atom   -> multiply
    ?atom: NUMBER           -> number
         | "(" expression ")"
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

advent_of_code_plus_first_grammar = """
    ?start: expression
    ?expression: sum
        | sum "*" expression   -> multiply
    ?sum: atom
        | sum "+" atom   -> add
    ?atom: NUMBER           -> number
         | "(" expression ")"
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    def number(self, input):
        return int(input)
    def multiply(self, input0, input1):
        return input0 * input1
    def add(self, input0, input1):
        return input0 + input1

aoc_left_to_right_parser = Lark(advent_of_code_left_to_right_grammar, parser='lalr', transformer=CalculateTree())
aoc_plus_first_parser = Lark(advent_of_code_plus_first_grammar, parser='lalr', transformer=CalculateTree())

def evaluate(line: str, plusHasPrecedence = False) -> int:
    parser = aoc_plus_first_parser if plusHasPrecedence else aoc_left_to_right_parser
    return parser.parse(line)

with open(abspath(join(dirname(__file__), 'input'))) as f:
    lines = [l.strip() for l in f.readlines()]

def part1() -> int:
    return sum([evaluate(line) for line in lines])

def part2() -> int:
    return sum([evaluate(line, True) for line in lines])

print("Part 1:", part1())
print("Part 2:", part2())