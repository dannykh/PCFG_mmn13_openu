from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.cnf import binarization, revert_binarization
from src.util.tree.node import Node


def write_tree(node: Node) -> str:
    """
    Transform tree to a sequence of tags.
    :param node: Tree's head
    :return : A string representation of the parse tree in bracketed notation.
    """
    if not node.children:
        return node.tag
    return "({} {})".format(node.tag, " ".join([write_tree(child) for child in node.children]))


if __name__ == '__main__':
    sent = "(TOP (S (S (NP (NN PCIPIZM)) (ADVP (RB AINW)) (VP (VB MWGBL)) (PP (IN B) (NP (NNP AIWBH))) (PP (IN L) " \
           "(NP (NP (NN SJWDNJIM)) (ADJP (JJ RDIQLIIM))))) (yyCM yyCM) (S (VP (VB APFR)) (VP (VB LMCWA) (NP (AT AWT)" \
           " (NP (PRP HWA))) (PP (MOD GM) (PP (IN BIN) (NP (NP (NN XQLAIM)) (CC W) (NP (NNT PWELI) (NP (NN XRWFT))))))))" \
           " (yyDOT yyDOT)))"
    # sent = "(TOP (S (yyQUOT yyQUOT) (S (VP (VB THIH)) (NP (NN NQMH)) (CC W) (ADVP (RB BGDWL))) (yyDOT yyDOT)))"
    head = node_tree_from_sequence(sent)
    print(sent)
    orig = write_tree(head)
    print(write_tree(head))
    binarization(head,2,2)
    reversed_tree = write_tree(head)
    print(write_tree(head))
    revert_binarization(head)
    reverted = write_tree(head)
    print(write_tree(head))
    assert reverted == orig
    assert orig != reversed_tree
