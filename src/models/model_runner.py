import os

from src.models.parser_with_precolation import ParserWithPrecolation
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.get_yield import get_yield
from src.util.tree.treebank import read_corpus

if __name__ == '__main__':
    path_to_gold = "../../data/heb-ctrees_under_10.gold"
    model = ParserWithPrecolation()
    if not os.path.isfile(model.pkl_path):
        corpus = read_corpus("../../data/heb-ctrees.train")
        model.train(corpus)
    else:
        model.load_from_pickle()
    gold_corp = read_corpus(path_to_gold)
    clean_sentences = [list(map(lambda node: node.tag, get_yield(node_tree_from_sequence(sent)))) for sent in gold_corp]
    model.write_parse(clean_sentences, "../../output/{}.txt".format(model.__class__.__name__), versbose=True)
