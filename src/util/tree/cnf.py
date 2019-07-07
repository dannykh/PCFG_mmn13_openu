from typing import List, Tuple

from src.util.tree.builders import node_tree_from_sequence
from src.util.tree.node import Node


def horizontal_binarization(root: Node, horz_lim: int = 999) -> Node:
    """
    Transforms a tree of any shape to a binary tree.
    :param root: The root of the tree.
    :param horz_lim: Limit of number of brothers to remember in history.
    :return: None. Alters the given tree, making it binary by adding "fake" non-terminals, following the binarization
             scheme proposed in class (lecture #6).
    """
    node_list = [(root, [], 0)]
    while node_list:
        node, brothers, split_index = node_list.pop()
        if node is None or (not brothers and not node.children):
            continue
        if not brothers:
            children = node.children
            if len(children) <= 2:
                lchild = children[0]
                rchild = children[1] if len(children) >= 2 else None
            else:
                lchild = children[0]
                rchild = Node("{}*{}".format(lchild.tag, "-".join([child.tag for child in children[1:]])))
                node.children = [lchild, rchild]
                brothers = children
                split_index = 1

        else:
            lchild = brothers[split_index]
            if len(brothers) - split_index == 2:
                rchild = brothers[-1]
                brothers = []
                split_index = 0
            else:
                split_index += 1
                rchild = Node("{}*{}".format("-".join([child.tag for child in brothers[:split_index]]),
                                             "-".join([child.tag for child in brothers[split_index:]])))
            node.children = [lchild, rchild]
        node_list += [(lchild, [], 0), (rchild, brothers, split_index)]
    return root


def revert_horizontal_binarization(root: Node) -> Node:
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
        # Search for the fake annotation marker, except in leaves (terminals)
        if node.children and "*" in node.tag:
            node_list += [(child, parent) for child in node.children]
        else:
            if parent is not None:
                parent.add_child(node)
            node_list += [(child, node) for child in node.children]
        node.children = []

    return root


# def un_chomsky_normal_form(tree, expandUnary=True, childChar="|", parentChar="^", unaryChar="+"):
#     # Traverse the tree-depth first keeping a pointer to the parent for modification purposes.
#     nodeList = [(tree, [])]
#     while nodeList != []:
#         node, parent = nodeList.pop()
#         if isinstance(node, Tree):
#             # if the node contains the 'childChar' character it means that
#             # it is an artificial node and can be removed, although we still need
#             # to move its children to its parent
#             childIndex = node.label().find(childChar)
#             if childIndex != -1:
#                 nodeIndex = parent.index(node)
#                 parent.remove(parent[nodeIndex])
#                 # Generated node was on the left if the nodeIndex is 0 which
#                 # means the grammar was left factored.  We must insert the children
#                 # at the beginning of the parent's children
#                 if nodeIndex == 0:
#                     parent.insert(0, node[0])
#                     parent.insert(1, node[1])
#                 else:
#                     parent.extend([node[0], node[1]])
#
#                 # parent is now the current node so the children of parent will be added to the agenda
#                 node = parent
#             else:
#                 parentIndex = node.label().find(parentChar)
#                 if parentIndex != -1:
#                     # strip the node name of the parent annotation
#                     node.set_label(node.label()[:parentIndex])
#
#                 # expand collapsed unary productions
#                 if expandUnary == True:
#                     unaryIndex = node.label().find(unaryChar)
#                     if unaryIndex != -1:
#                         newNode = Tree(
#                             node.label()[unaryIndex + 1:], [i for i in node]
#                         )
#                         node.set_label(node.label()[:unaryIndex])
#                         node[0:] = [newNode]
#
#             for child in node:
#                 nodeList.append((child, node))


# def collapse_unary(tree, collapsePOS=False, collapseRoot=False, joinChar="+"):
#     """
#     Collapse subtrees with a single child (ie. unary productions)
#     into a new non-terminal (Tree node) joined by 'joinChar'.
#     This is useful when working with algorithms that do not allow
#     unary productions, and completely removing the unary productions
#     would require loss of useful information.  The Tree is modified
#     directly (since it is passed by reference) and no value is returned.
#
#     :param tree: The Tree to be collapsed
#     :type  tree: Tree
#     :param collapsePOS: 'False' (default) will not collapse the parent of leaf nodes (ie.
#                         Part-of-Speech tags) since they are always unary productions
#     :type  collapsePOS: bool
#     :param collapseRoot: 'False' (default) will not modify the root production
#                          if it is unary.  For the Penn WSJ treebank corpus, this corresponds
#                          to the TOP -> productions.
#     :type collapseRoot: bool
#     :param joinChar: A string used to connect collapsed node values (default = "+")
#     :type  joinChar: str
#     """
#
#     if collapseRoot == False and isinstance(tree, Tree) and len(tree) == 1:
#         nodeList = [tree[0]]
#     else:
#         nodeList = [tree]
#
#     # depth-first traversal of tree
#     while nodeList != []:
#         node = nodeList.pop()
#         if isinstance(node, Tree):
#             if (
#                     len(node) == 1
#                     and isinstance(node[0], Tree)
#                     and (collapsePOS == True or isinstance(node[0, 0], Tree))
#             ):
#                 node.set_label(node.label() + joinChar + node[0].label())
#                 node[0:] = [child for child in node[0]]
#                 # since we assigned the child's children to the current node,
#                 # evaluate the current node again
#                 nodeList.append(node)
#             else:
#                 for child in node:
#                     nodeList.append(child)

if __name__ == '__main__':
    sent = "(TOP (S (yyQUOT yyQUOT) (S (VP (VB THIH)) (NP (NN NQMH)) (CC W) (ADVP (RB BGDWL))) (yyDOT yyDOT)))"
    head = node_tree_from_sequence(sent)
    horizontal_binarization(head)
