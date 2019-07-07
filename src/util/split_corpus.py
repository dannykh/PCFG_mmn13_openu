from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.get_yield import get_yield
from src.util.tree.treebank import read_corpus


def generate_corpus_in_bounds(from_length: int, to_length: int, base_fpath="../../data/heb-ctrees.gold"):
    """
    Generate a corpus file of a corpus from within a given corpus, with sentences limited by length in specified bounds.
    :param from_length : Minimum sentence length.
    :param to_length: Length of sentences.
    :param base_fpath: Path to base corpus
    :return: Path to newly generated corpus.
    """
    new_fpath = base_fpath.replace(".gold", "_{}-{}.gold".format(from_length, to_length))
    with open(new_fpath, "w") as fp:
        for sent in read_corpus(base_fpath):
            if from_length <= len(get_yield(node_tree_from_sequence(sent))) <= to_length:
                fp.write(sent + "\n")

    return new_fpath


if __name__ == '__main__':
    generate_corpus_in_bounds(10, 20)
