import os
import time

from src.models.parser_with_precolation import ParserWithPrecolation
from src.util.split_corpus import generate_corpus_in_bounds
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.get_yield import get_yield
from src.util.tree.treebank import read_corpus

override = False

if __name__ == '__main__':
    model_list = [ParserWithPrecolation()]
    len_bounds_list = ((0, 10), (11, 20), (21, 25), (25, 30), (30, 35), (35, 40))

    for model in model_list:
        print("Running {} :".format(model.__class__.__name__))
        if not os.path.isfile(model.pkl_path):
            corpus = read_corpus("../../data/heb-ctrees.train")
            model.train(corpus)
        else:
            model.load_from_pickle()
        for min_len, max_len in len_bounds_list:
            out_path = "../../output/{}_{}-{}.txt".format(model.__class__.__name__, min_len, max_len)
            if not override and os.path.isfile(out_path):
                continue
            path_to_gold = generate_corpus_in_bounds(min_len, max_len)
            gold_corp = read_corpus(path_to_gold)
            clean_sentences = [list(map(lambda node: node.tag, get_yield(node_tree_from_sequence(sent)))) for sent in
                               gold_corp]
            st = time.monotonic()
            model.write_parse(clean_sentences, out_path, versbose=True)
            print("Total time : {} \n".format(time.monotonic() - st))
