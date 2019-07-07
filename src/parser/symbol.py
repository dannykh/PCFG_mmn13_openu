from typing import List, Tuple


class Symbol:
    """
    An abstract symbol.
    """

    def __init__(self, symbol_string: str):
        self.symbol_string = symbol_string

    def __str__(self):
        return self.symbol_string

    def __eq__(self, other: "Symbol"):
        return self.symbol_string == other.symbol_string and type(self) == type(other)

    def __hash__(self):
        return hash(self.symbol_string)


class Terminal(Symbol):
    """
    A terminal symbol.
    """

    def __init__(self, symbol_string: str): super().__init__(symbol_string)


class NonTerminal(Symbol):
    """
    A non-terminal symbol.
    """

    def __init__(self, symbol_string: str): super().__init__(symbol_string)


class MultiSymbol:
    """
    An ordered list of symbols, representing a derivation participant (LHS or RHS).
    """

    def __init__(self, symbols: Tuple[Symbol, ...]):
        self.symbol_list: Tuple[Symbol, ...] = symbols

    def __eq__(self, other: "MultiSymbol"):
        return self.symbol_list == other.symbol_list

    def __str__(self):
        return ' '.join([sym.symbol_string for sym in self.symbol_list])

    def __add__(self, other: "MultiSymbol"):
        # Adding multi symbols means concatenating their symbol lists
        return MultiSymbol(self.symbol_list + other.symbol_list)

    def __hash__(self):
        return hash("".join(map(str, self.symbol_list)))

    def __getitem__(self, item: int):
        return self.symbol_list[item]
