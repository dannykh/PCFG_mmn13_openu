from typing import List


class Node:

    def __init__(self, tag: str):
        self.tag: str = tag
        self.children: List[Node] = []
        # print(f'node created with tag {tag}')

    def add_child(self, child: "Node"):
        self.children.append(child)

    def remove_child(self, child: "Node"):
        self.children.remove(child)

    def get_downward_arcs(self):
        return self._get_arcs()

    def _get_arcs(self):
        arcs = []
        for child in self.children:
            arc = (self.tag, child.tag)
            arcs.append(arc)
            arcs.extend(child._get_arcs())

        return arcs
