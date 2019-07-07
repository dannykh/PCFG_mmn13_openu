import copy
from typing import NamedTuple, Dict, Tuple

from math import inf, sqrt

from src.parser.grammar import ProbGrammar, write_grammar_to_files, pickle_grammar, unpickle_grammar, precolate_grammar
from src.parser.parser_model import PCFGModel
from src.parser.symbol import Symbol, MultiSymbol, Terminal, NonTerminal
from src.parser.train import TreeTransformationPipeline, GrammarTransformationPipeline
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.cnf import horizontal_binarization, revert_horizontal_binarization
from src.util.tree.get_yield import get_yield
from src.util.tree.node import Node
from src.util.tree.treebank import read_corpus
from src.util.tree.writer import write_tree

# TODO : Move elsewhere.
# For simplicity, unseen tokens shall be marked as NN
# Possible improvement : HMM\MEMM with some smoothing?
UNK_SYMBOL = NonTerminal("NN")

CkyTableEntry = NamedTuple("CkyTableEntry", [("node", Node), ("minus_log_prob", float)])


def cky(grammar: ProbGrammar, sentence: str, include_unary=False) -> Node:
    """
    An implementation of CKY algorithm in it's wikipedia version.
    :param grammar: The probabilistic grammar to use.
    :param sentence: A sentence of lexical tokens separated by white space.
    :param include_unary: True if to support unary rules in run, False otherwise.
    :return: Most probable parse tree for given sentence.
    """
    sentence = sentence.split(" ")
    n = len(sentence)
    cky_table: Dict[Tuple[int, int], Dict[MultiSymbol, CkyTableEntry]] = {(i, j): dict() for i in range(n + 1) for j in
                                                                          range(n + 1)}
    for j in range(0, n):
        rhs = MultiSymbol((Terminal(sentence[j]),))
        terminal_node = Node(sentence[j])
        cky_table[0, j][rhs] = CkyTableEntry(terminal_node, -0.0)
        # Check if symbol exists as some rule's RHS in grammar
        if rhs in grammar.rhs_to_lhs_map:
            # Iterate all rules generating this as rhs
            for rule in grammar.rhs_to_lhs_map[rhs]:
                assert rule.is_lexical()  # Sanity check
                node = Node(str(rule.lhs))
                node.add_child(terminal_node)
                cky_table[1, j][rule.lhs] = CkyTableEntry(node, grammar[rule].minus_log_prob)
        else:
            # Initiate assuming no match in lexical rules in grammar, and therefore UNK symbol most probable
            # (See note near definition of UNK_SYMBOL )
            node = Node(str(UNK_SYMBOL))
            node.add_child(terminal_node)
            cky_table[1, j][MultiSymbol((UNK_SYMBOL,))] = CkyTableEntry(node, -0.0)

    for span_length in range(2, n + 1):
        for span_start in range(0, n - span_length + 1):
            for partition in range(1, span_length):
                # Name current entries in table as B, C for possible derivation " _ -> B C "
                for rhs_B, rhs_B_entry in cky_table[partition, span_start].items():
                    for rhs_C, rhs_C_entry in \
                            cky_table[span_length - partition, span_start + partition].items():
                        if rhs_B_entry.minus_log_prob + rhs_C_entry.minus_log_prob > 50:
                            continue
                        # Build RHS as concatenation of B and C
                        rhs = rhs_B + rhs_C
                        # Skip if no rule exists such that -> B C
                        if rhs not in grammar.rhs_to_lhs_map:
                            continue
                        # There are rules A -> B C in grammar, add all such rules as possible derivations
                        for rule in grammar.rhs_to_lhs_map[rhs]:
                            rule_prob = rhs_B_entry.minus_log_prob + rhs_C_entry.minus_log_prob + grammar[
                                rule].minus_log_prob
                            if rule.lhs not in cky_table[span_length, span_start] or rule_prob < \
                                    cky_table[span_length, span_start][rule.lhs].minus_log_prob:
                                node = Node(str(rule.lhs))
                                node.add_child(rhs_B_entry.node)
                                node.add_child(rhs_C_entry.node)
                                cky_table[span_length, span_start][rule.lhs] = CkyTableEntry(node, rule_prob)

    return min([(node, prob) for _, (node, prob) in cky_table[n, 0].items() if
                node.tag in map(str, grammar.start_symbols)], key=lambda x: x[1])[0]


def add_top(head: Node) -> Node:
    new_head = Node("TOP")
    new_head.add_child(head)
    return new_head


if __name__ == '__main__':
    tree_transformer = TreeTransformationPipeline([
        ("Binarize", horizontal_binarization)
    ])
    tree_detransformer = TreeTransformationPipeline([
        ("add TOP", add_top),
        ("de_binarize", revert_horizontal_binarization)
    ])
    grammar_transformer = GrammarTransformationPipeline([
        ("precolation", precolate_grammar)
    ])
    grammar = unpickle_grammar("../../exps/model.pkl")
    model = PCFGModel(tree_transformer, tree_detransformer, grammar_transformer, cky, grammar=grammar)
    # model.fit(read_corpus("../../data/heb-ctrees.train"))
    # grammar = model.grammar
    # pickle_grammar(grammar, "../../exps/model.pkl")
    # write_grammar_to_files(grammar, "../../exps/train.gram", "../../exps/train.lex")
    limit = 2
    gold_corp = read_corpus("../../data/heb-ctrees.gold")
    with open("../../output/gold_tagged_1.txt", "w") as wfp:
        for sent in gold_corp:
            if limit <= 0:
                break
            limit -= 1
            sent = " ".join(map(lambda node: node.tag, get_yield(node_tree_from_sequence(sent))))
            try:
                decoded = model.decode(sent)
                wfp.write(write_tree(decoded) + "\n")
            except Exception as e:
                print("FAILED {} \n {}".format(sent, e))
