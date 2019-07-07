from typing import Iterator

from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.node import Node

StringCorpus = Iterator[str]


def read_corpus(corpus_path: str, limit=999999) -> StringCorpus:
    """
    Iterate corpus line by line.
    :param corpus_path: Path to file to read.
    :param limit : max sentences to read
    :return: An iterator of lines in the file (string)
    """
    with open(corpus_path, "r") as fp:
        for line in fp:
            if limit <= 0:
                break
            limit -= 1
            yield line.strip()


def get_trees_from_corpus(corpus: StringCorpus) -> Iterator[Node]:
    """
    Iterate a corpus and yield a tree of eah of it's sentences.
    :param corpus: An iterable sequence of sentences (strings) in bracketed notation.
    :return: An iterator of trees (Node) generated from each line of the corpus.
    """
    for sentence in corpus:
        yield node_tree_from_sequence(sentence)
