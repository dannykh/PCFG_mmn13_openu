import time
from typing import Callable, List

from src.parser.grammar import ProbGrammar
from src.parser.train import TreeTransformationPipeline, GrammarTransformationPipeline
from src.parser.tree_parser import get_rules_from_tree
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.node import Node
from src.util.tree.treebank import StringCorpus
from src.util.tree.writer import write_tree


class ParserModel:
    """
    A PCFG parser model, trained on a corpus (of bracket notation sequences) using it's transformation pipelines,
    transforming trees and the generated grammar.
    After training (applying fit on a corpus or loading an existing grammar), a sentence is tagged using the grammar,
    after applying supplied detransformers to the sentence.

    The training is as follows :
    The given text corpus is iterated sentence by sentence, each transformed into a basic tree and then transformed
    using the supplied transformation pipeline. Rules are extracted from the resulting tree and are added to
    the base grammar (which is built incrementally).

    The model can be supplied an initial grammar ( if, for instance, loading a pre-trained model).

    Decoding is as follows :
    The given sentence is transformed to a basic tree, which is transformed using the model's tree transformation
    pipeline. The transformed tree is then decoded using the decode algorithm given.

    Notes :
    1) tree_detransformation_pipeline should revert all alterations done by tree_transformation_pipeline,
        such that  tree_detransformation_pipeline((tree_transformation_pipeline(T)) = T.
    2) grammar_transformation_pipeline is added to allow for easy manipulation of the base generated grammar.
    """

    def __init__(self, tree_transformation_pipeline: TreeTransformationPipeline,
                 tree_detransformation_pipeline: TreeTransformationPipeline,
                 grammar_transformation_pipeline: GrammarTransformationPipeline,
                 decode_algorithm: Callable[[ProbGrammar, List[str]], Node], grammar: ProbGrammar = None):
        self.grammar: ProbGrammar = ProbGrammar() if grammar is None else grammar
        self.tree_transformation_pipeline = tree_transformation_pipeline
        self.tree_detransformation_pipeline = tree_detransformation_pipeline
        self.grammar_transformation_pipline = grammar_transformation_pipeline
        self.decode_alg = decode_algorithm

    def train(self, corpus: StringCorpus, verbose=True):
        """
        Train the model on a given corpus.
        :param corpus: The corpus with whcih to train.
        :param verbose: Whether to log.
        :return: None.

        The corpus is traversed sequence by sequence, a tree is generated from each sequence, on which the
        tree_transformation_pipeline is applied (where, for instance, binarization should occur), rules are generated
        from the tree and added to the grammar. Once all rules from all sequences in the corpus have been added to
        the grammar, rule probabilities are generated, AFTER WHICH the grammar_transformation_pipeline is applied
        to the grammar (where, for instance, unary rule precolation could occur).
        """
        self.grammar = ProbGrammar()  # Clear grammar
        for i, sentence in enumerate(corpus, 1):
            if verbose:
                print("{}".format(i))
            sent_tree = node_tree_from_sequence(sentence)
            sent_tree = self.tree_transformation_pipeline.transform(sent_tree)
            for rule in get_rules_from_tree(sent_tree):
                self.grammar.add_rule(rule)
        self.grammar.generate_rule_probabilities()
        self.grammar = self.grammar_transformation_pipline.transform(self.grammar)

    def decode(self, sentence: List[str]) -> Node:
        tree = self.decode_alg(self.grammar, sentence)
        return self.tree_detransformation_pipeline.transform(tree)

    def write_parse(self, corpus: List[List[str]], output_treebank_file: str, versbose=False):
        with open(output_treebank_file, "w") as fp:
            for i, sentence in enumerate(corpus, 1):
                ts = time.monotonic()
                fp.write(write_tree(self.decode(sentence)) + "\n")
                if versbose:
                    print("{} took {} seconds ".format(i, time.monotonic() - ts))
