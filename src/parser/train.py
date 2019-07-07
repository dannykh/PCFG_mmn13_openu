from typing import List, Tuple, Callable

from src.parser.grammar import ProbGrammar
from src.util.tree.node import Node


class TreeTransformationPipeline:
    """
    A pipeline of tree transformations
    """

    def __init__(self, transformer_list: List[Tuple[str, Callable[[Node], Node]]]):
        self.transformer_list: List[Tuple[str, Callable[[Node], Node]]] = transformer_list

    def transform(self, tree_root: Node, verbose=False) -> Node:
        for transformer_name, transformer in self.transformer_list:
            if verbose:
                print(transformer_name)
            tree_root = transformer(tree_root)
        return tree_root


class GrammarTransformationPipeline:
    """
    A pipeline of functions, transforming a string corpus into a probabilistic grammar (ProbGrammar).
    """

    def __init__(self, transformers: List[Tuple[str, Callable[[ProbGrammar], ProbGrammar]]]):
        self.transformers = transformers

    def transform(self, grammar: ProbGrammar, verbose=False):
        for transformer_name, transformer in self.transformers:
            if verbose:
                print(transformer_name)
            grammar = transformer(grammar)
        return grammar
