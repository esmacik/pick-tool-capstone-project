from graph.node import Node


class Relationship:

    def __init__(self, id, label, parent_node=None, child_node=None):
        self.id = id
        self.label = label
        self.parent_node = parent_node
        self.child_node = child_node

    # Set the child and parent for this relationship.
    def set_child_parent(self, parent_node=None, child_node=None):
        if parent_node is not None:
            self.parent_node = parent_node
        if child_node is not None:
            self.child_node = child_node

    # Set the description label for this relationship.
    def set_label(self, label):
        self.label = label

    # Get a list of nodes associated to this relationship
    def get_nodes(self):
        return [self.parent_node, self.child_node]
