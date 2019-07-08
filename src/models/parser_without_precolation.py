from src.parser.cky import add_top, cky
from src.parser.grammar import precolate_grammar
from src.parser.parser_model import ParserModel
from src.parser.train import TreeTransformationPipeline, GrammarTransformationPipeline
from src.util.tree.cnf import horizontal_binarization, revert_horizontal_binarization

tree_transformer = TreeTransformationPipeline([
    ("Binarize", horizontal_binarization)
])
tree_detransformer = TreeTransformationPipeline([
    ("add TOP", add_top),
    ("de_binarize", revert_horizontal_binarization)
])
grammar_transformer = GrammarTransformationPipeline([
])


class ParserWithoutPrecolation(ParserModel):
    def __init__(self):
        super().__init__(tree_transformer, tree_detransformer, grammar_transformer,
                         lambda gram, sent: cky(gram, sent, True))
        self.pkl_path = "../../exps/ParserWithoutPrecolation.pkl"
