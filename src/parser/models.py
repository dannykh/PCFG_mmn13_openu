from src.parser.cky import add_top, cky
from src.parser.grammar import precolate_grammar
from src.parser.parser_model import ParserModel
from src.parser.pipeline import TreeTransformationPipeline, GrammarTransformationPipeline
from src.util.tree.cnf import binarization, revert_binarization

tree_no_vert_max_horiz_transformer = TreeTransformationPipeline([
    ("Binarize", binarization)
])

tree_1_vert_max_horiz_transformer = TreeTransformationPipeline([
    ("Binarize", lambda root: binarization(root, 1))
])

tree_1_vert_2_horiz_transformer = TreeTransformationPipeline([
    ("Binarize", lambda root: binarization(root, 1, 2))
])

tree_detransformer = TreeTransformationPipeline([
    ("add TOP", add_top),
    ("de_binarize", revert_binarization)
])
grammar_no_precolation_transformer = GrammarTransformationPipeline([
])

grammar_precolation_transformer = GrammarTransformationPipeline([
    ("precolation", precolate_grammar)
])


class P0VCMHC(ParserModel):
    """
    Precolation, 0 vertical context, maximum horizontal context
    """

    def __init__(self):
        super().__init__(tree_no_vert_max_horiz_transformer, tree_detransformer, grammar_precolation_transformer,
                         lambda gram, sent: cky(gram, sent, False))
        self.pkl_path = "../../exps/parser_P_0VC_MHC.pkl"


class NP0VCMHC(ParserModel):
    """
    No precolation, 0 vertical context, maximum horizontal context
    """

    def __init__(self):
        super().__init__(tree_no_vert_max_horiz_transformer, tree_detransformer, grammar_no_precolation_transformer,
                         lambda gram, sent: cky(gram, sent, True))
        self.pkl_path = "../../exps/parser_NP_0VC_MHC.pkl"


class NP1VCMHC(ParserModel):
    """
    No precolation, 1 vertical context, maximum horizontal context
    """

    def __init__(self):
        super().__init__(tree_1_vert_max_horiz_transformer, tree_detransformer, grammar_no_precolation_transformer,
                         lambda gram, sent: cky(gram, sent, True))
        self.pkl_path = "../../exps/parser_NP_1VC_MHC.pkl"


class NP1VC2HC(ParserModel):
    """
    No precolation, 1 vertical context, 2 horizontal context
    """

    def __init__(self):
        super().__init__(tree_1_vert_2_horiz_transformer, tree_detransformer, grammar_no_precolation_transformer,
                         lambda gram, sent: cky(gram, sent, True))
        self.pkl_path = "../../exps/parser_NP_1VC_2HC.pkl"
