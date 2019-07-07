from typing import List, Type

from src.parser.symbol import Symbol, Terminal, NonTerminal, MultiSymbol


class Rule:
    """
    A derivation rule, lexical or grammatical.
    The rule is represented as rewrite of a sequence of left hand side (lhs) symbols (strings) into a sequence of
    right hand side (rhs) symbols.
    """

    def __init__(self, lhs_symbol: MultiSymbol, rhs_symbol: MultiSymbol):
        self.lhs: MultiSymbol = lhs_symbol
        self.rhs: MultiSymbol = rhs_symbol

    def is_unary(self):
        return len(self.lhs.symbol_list) == 1 and len(self.rhs.symbol_list) == 1

    def is_lexical(self):
        return all(map(lambda x: type(x) is Terminal, self.rhs.symbol_list))

    def __str__(self):
        return "{} --> {}".format(str(self.lhs), str(self.rhs))

    def __hash__(self):
        return hash("".join(map(str, (self.lhs.symbol_list + self.rhs.symbol_list))))

    def __eq__(self, other: "Rule"):
        return self.lhs == other.lhs and self.rhs == other.rhs


if __name__ == '__main__':
    pass
