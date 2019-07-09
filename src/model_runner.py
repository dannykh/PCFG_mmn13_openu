import os
import time

from src.parser.grammar import unpickle_grammar, pickle_grammar, write_grammar_to_files
from src.parser.models import NP1VC2HC
from src.util.split_corpus import generate_corpus_in_bounds
from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.get_yield import get_yield
from src.util.tree.treebank import read_corpus

override_existing_run = False
train_path = "../data/heb-ctrees.train"
gold_path = "../data/heb-ctrees.gold"

if __name__ == '__main__':
    model_list = [NP1VC2HC()]
    len_bounds_list = ((0, 10), (11, 20), (21, 25), (25, 30), (30, 35), (35, 40))

    for model in model_list:
        model_name = model.__class__.__name__
        model_out_dir_name = "../output/{}/".format(model_name)
        pkl_path = model_out_dir_name + "{}_grammar.pkl".format(model_name)
        print("Running {} :".format(model_name))
        if not os.path.isdir(model_out_dir_name):
            os.mkdir(model_out_dir_name)
        if not os.path.isfile(pkl_path):
            print("Training Model : ")
            corpus = read_corpus(gold_path)
            model.train(corpus)
            pickle_grammar(model.grammar, pkl_path)
            write_grammar_to_files(model.grammar, *map(
                lambda ftype: model_out_dir_name + "{}.{}".format(model_name, ftype), ("gram", "lex")))
        else:
            model.grammar = unpickle_grammar(pkl_path)
        for min_len, max_len in len_bounds_list:
            out_path = model_out_dir_name + "{}_{}-{}.txt".format(model_name, min_len, max_len)
            if not override_existing_run and os.path.isfile(out_path):
                continue
            path_to_gold = generate_corpus_in_bounds(min_len, max_len, gold_path)
            gold_corp = read_corpus(path_to_gold)
            clean_sentences = [list(map(lambda node: node.tag, get_yield(node_tree_from_sequence(sent)))) for sent in
                               gold_corp]
            st = time.monotonic()
            model.write_parse(clean_sentences, out_path, versbose=True)
            print("Total time : {} \n".format(time.monotonic() - st))
