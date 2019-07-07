from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.get_yield import get_yield
from src.util.tree.treebank import read_corpus


def generate_corpus_with_limit(sentence_limit: int, base_fpath="../../data/heb-ctrees.gold"):
    """
    Generate a corpus file of a corpus from within a given corpus, with sentences limited to a max length
    :param sentence_limit: Length of sentences.
    :param base_fpath: Path to base corpus
    :return: Path to newly generated corpus.
    """
    new_fpath = base_fpath.replace(".gold", "_under_{}.gold".format(sentence_limit))
    with open(new_fpath, "w") as fp:
        for sent in read_corpus(base_fpath):
            if len(get_yield(node_tree_from_sequence(sent))) < sentence_limit:
                fp.write(sent + "\n")

    return new_fpath


if __name__ == '__main__':
    generate_corpus_with_limit(10)
