from typing import List, Tuple

from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.node import Node

parent_separator = "|"
brother_separator = "*"
join_symbol = "-"


def binarization(root: Node, vertical_hist: int = 0, horizontal_smoothing: int = 999) -> Node:
    """
    Transforms a tree of any shape to a binary tree.
    :param root: The root of the tree.
    :param horizontal_smoothing: Limit of number of brothers to remember in history.
    :param vertical_hist : Number of parents to add as context in tag.
    :return: None. Alters the given tree, making it binary by adding "fake" non-terminals, following the binarization
             scheme proposed in class (lecture #6).
    """
    node_list = [(root, ["TOP"] if vertical_hist > 0 else [], [], 0)]
    while node_list:
        node, parents, brothers, split_index = node_list.pop()
        if node is None or (not brothers and not node.children):
            continue
        orig_tag = node.tag
        node.tag = "{}{}{}".format(join_symbol.join(parents), parent_separator, node.tag)
        if not brothers:
            children = node.children
            if len(children) <= 2:
                lchild = children[0]
                rchild = children[1] if len(children) >= 2 else None
            else:
                lchild = children[0]
                rchild = Node("{}*{}".format(lchild.tag, join_symbol.join(
                    [child.tag for child in children[1:horizontal_smoothing + 1]])))
                node.children = [lchild, rchild]
                brothers = children
                split_index = 1
            parents = (parents + [orig_tag])[-vertical_hist:]

        else:
            lchild = brothers[split_index]
            if len(brothers) - split_index == 2:
                rchild = brothers[-1]
                brothers = []
                split_index = 0
            else:
                split_index += 1
                rchild = Node("{}*{}".format(
                    "-".join(
                        [child.tag for child in brothers[max(0, split_index - horizontal_smoothing + 1):split_index]]),
                    "-".join([child.tag for child in brothers[split_index:split_index + horizontal_smoothing]])))
            node.children = [lchild, rchild]
        node_list += [(lchild, parents, [], 0), (rchild, parents, brothers, split_index)]
    return root


def revert_binarization(root: Node) -> Node:
    """
    Revert a binarized tree to it's original form. Assuming * annotation used for "fake" nodes.
    :param root: Root of the binarized tree.
    :return: None, alters the given tree.
    """
    node_list: List[Tuple[Node, Node]] = [(root, Node("STUB"))]
    while node_list:
        node, parent = node_list.pop(0)
        if node is None:
            continue
        node.tag = node.tag if parent_separator not in node.tag else "".join(node.tag.split(parent_separator)[1])
        # Search for the fake annotation marker, except in leaves (terminals)
        if node.children and brother_separator in node.tag:
            node_list += [(child, parent) for child in node.children]
        else:
            if parent is not None:
                parent.add_child(node)
            node_list += [(child, node) for child in node.children]
        node.children = []

    return root


if __name__ == '__main__':
    sent = "(TOP (S (yyQUOT yyQUOT) (S (VP (VB THIH)) (NP (NN NQMH)) (CC W) (ADVP (RB BGDWL))) (yyDOT yyDOT)))"
    head = node_tree_from_sequence(sent)
    binarization(head)
    # print(write_tree(head))
