from os.path import abspath, dirname, join
from typing import List, Tuple

from sly import Lexer, Parser

class AdventOfCodeLexer(Lexer):
    tokens = { NUMBER, PLUS, TIMES, LPAREN, RPAREN }
    ignore = ' \t'

    # Tokens
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    TIMES = r'\*'
    LPAREN = r'\('
    RPAREN = r'\)'

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class AdventOfCodeParser(Parser):
    tokens = AdventOfCodeLexer.tokens
    precedence = (
        ('left', 'PLUS', 'TIMES'),
    )
    def __init__(self):
        self.result: int = None

    @_('expr')
    def statement(self, p):
        self.result = p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

class AdventOfCodePlusFirstParser(AdventOfCodeParser):
    precedence = (
        ('left', 'TIMES'),
        ('left', 'PLUS'), # tuple is bottom up, so plus is first here
    )

    # sly can't actually extend parsers right, so we copy and paste the functions from above (https://github.com/dabeaz/sly/issues/12)
    @_('expr')
    def statement(self, p):
        self.result = p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

def evaluate(line: str, plusHasPrecedence = False) -> int:
    lexer = AdventOfCodeLexer()
    parser = AdventOfCodePlusFirstParser() if plusHasPrecedence else AdventOfCodeParser()
    lexed_math = lexer.tokenize(line)
    parser.parse(lexed_math)
    return parser.result

with open(abspath(join(dirname(__file__), 'input'))) as f:
    lines = [l.strip() for l in f.readlines()]

def part1() -> int:
    return sum([evaluate(line) for line in lines])

def part2() -> int:
    return sum([evaluate(line, True) for line in lines])

print("Part 1:", part1())
print("Part 2:", part2())