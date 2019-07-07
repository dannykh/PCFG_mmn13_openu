from typing import Iterator

from src.parser.rule import Rule
from src.parser.symbol import MultiSymbol, NonTerminal, Terminal
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.node import Node


def get_rules_from_tree(root: Node) -> Iterator[Rule]:
    """
    Iterate over grammar rules generated from a given syntactic parse tree.
    :param root: Root node of the tree.
    :return: An iterator of derivations in tree (father->children)
    """
    node_list = [root]
    # BFS style traversal of tree
    while node_list:
        node = node_list.pop()
        lhs = MultiSymbol((NonTerminal(node.tag),))
        if not node.children:
            continue
        node_list += node.children
        rhs_symbols = ()
        for child in node.children:
            if child.children:  # not terminal:
                rhs_symbols = rhs_symbols + (NonTerminal(child.tag),)
            else:
                rhs_symbols = rhs_symbols + (Terminal(child.tag),)
        yield Rule(lhs, MultiSymbol(rhs_symbols))


if __name__ == '__main__':
    sent = "(TOP (S (ADVP (RB RCUB)) (ADVP*VP-PP-NP-yyDOT (VP (VB MWXZR)) (ADVP-VP*PP-NP-yyDOT (PP (IN ALI) " \
           "(NP (PRP ATM))) (ADVP-VP-PP*NP-yyDOT (NP (NP (H H) (NN XWMR)) (SBAR (REL F) (S (VP (VB NFLX))" \
           " (PP (IN AL) (NP (PRP ANI)))))) (yyDOT yyDOT))))))"
    head = node_tree_from_sequence(sent)
    for rule in get_rules_from_tree(head):
        print("{} {} {} ".format(rule, rule.is_unary(), rule.is_lexical()))
