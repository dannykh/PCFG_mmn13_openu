from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.cnf import horizontal_binarization, revert_horizontal_binarization
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
    sent = "(TOP (S (S (ADVP (IN EL) (PRP KN)) (VP (VB APFR)) (VP (VP (VB LQRWA) (NP (AT AT) (NP (yyQUOT yyQUOT) " \
           "(NP (NNP PWS)) (yyQUOT yyQUOT))) (ADVP (RB GM)) (ADVP (RB AXRT))) (CC W) (VP (VB LHBIN) (NP (AT AT)" \
           " (NP (NN DMWTW))) (PP (IN K) (NP (NP (NN HTGLMWTH)) (POS FL) (NP (NP (H H) (NN NPF)) (ADJP (H H) " \
           "(JJ GRMNIT)))))))) (yyCLN yyCLN) (S (NP (NP (H H) (NN PGANIWT)) (yyCM yyCM) (SBAR (REL F) (S (PP (IN KNGD) " \
           "(NP (PRP HIA))) (NP (PRP HWA)) (VP (VB MCIG)) (ADVP (RB KAN)) (NP (AT AT) (NP (H H) (NN NCRWT)))))) " \
           "(yyCM yyCM) (ADVP (RB AINH)) (VP (VB MAPIINT)) (NP (NP (MOD RQ) (NP (AT AT) (NP (NP (H H) (NN ILIDIM)) " \
           "(ADJP (H H) (JJ QANIBLIM))))) (yyCM yyCM) (CC ALA) (NP (MOD GM) (NP (AT AT) (NP (NP (NNP PWS)) (yyCM yyCM) " \
           "(NP (NP (H H) (NN GRMNI)) (ADJP (H H) (JJ MGALWMAN))) (yyCM yyCM) (NP (NP (H H) (NN AIF)) (ADJP (JJT MFWLL)" \
           " (NP (H H) (NN RXMIM)))) (yyCM yyCM) (NP (NP (NN AIF)) (ADJP (ADJP (JJ AKZR)) (CC W) (ADJP (JJ DWRSNI))) " \
           "(SBAR (REL H) (S (VP (VB MAMIN)) (SBAR (SBAR (COM KI) (S (VP (VB AIN)) (NP (NN GBWLWT)) (PP (IN L) " \
           "(NP (NN KWXW))))) (yyCM yyCM) (CC W) (SBAR (COM KI) (S (VP (VB IF)) (PP (IN B) (NP (NNT IKWLT) (NP (H H) " \
           "(NN ADM)))) (VP (VB LDET) (NP (NN HKL))))))))) (yyCM yyCM) (NP (NP (H H) (NN AIF)) (SBAR (REL H) " \
           "(S (S (VP (VB IWCA)) (VP (VB LKBWF) (NP (NN JRIJWRIH)))) (CC W) (S (VP (VB MQRIB)) (PP (IN EL) " \
           "(NP (NNT MZBX) (NP (NP (NN FAPTNWTW)) (ADJP (JJT XSRT) (NP (H H) (NN MECWRIM)))))) (NP (NNT XII) " \
           "(NP (NN ADM))) (PP (IN BLA) (SBAR (COM F) (S (VP (VB IXWF)) (NP (NP (NN CER)) (CC AW) " \
           "(NP (NN XRJH))))))))))))))) (yyDOT yyDOT)))"
    head = node_tree_from_sequence(sent)
    print(sent)
    orig = write_tree(head)
    print(write_tree(head))
    horizontal_binarization(head)
    reversed_tree = write_tree(head)
    print(write_tree(head))
    revert_horizontal_binarization(head)
    reverted = write_tree(head)
    print(write_tree(head))
    assert reverted == orig
    assert orig != reversed_tree
