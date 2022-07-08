# this class is used to create a tree structure


class Node:

    Nodes = []

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def add_child(self, child):
        self.Nodes.append(child)

    def getNodes(self):
        return self.Nodes