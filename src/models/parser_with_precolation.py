from src.parser.cky import add_top, cky
from src.parser.grammar import precolate_grammar, unpickle_grammar, pickle_grammar
from src.parser.parser_model import ParserModel
from src.parser.train import TreeTransformationPipeline, GrammarTransformationPipeline
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.cnf import horizontal_binarization, revert_horizontal_binarization
from src.util.tree.get_yield import get_yield
from src.util.tree.treebank import read_corpus, StringCorpus
from src.util.tree.writer import write_tree

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


class ParserWithPrecolation(ParserModel):
    def __init__(self):
        super().__init__(tree_transformer, tree_detransformer, grammar_transformer,
                         lambda gram, sent: cky(gram, sent, False))
        self.pkl_path = "../../exps/ParserWithPrecolation.pkl"


if __name__ == '__main__':
    grammar = unpickle_grammar("../../exps/model.pkl")
    model = ParserWithPrecolation()
    model.grammar = grammar
    # model.train(read_corpus("../../data/heb-ctrees.train"))
    # pickle_grammar(model.grammar, "../../exps/model.pkl")
    # write_grammar_to_files(grammar, "../../exps/train.gram", "../../exps/train.lex")
    gold_corp = read_corpus("../../data/heb-ctrees.train", limit=2)
    corp = [list(map(lambda node: node.tag, get_yield(node_tree_from_sequence(sent)))) for sent in gold_corp]
    model.write_parse(corp, "../../output/gold_tagged_1.txt")
