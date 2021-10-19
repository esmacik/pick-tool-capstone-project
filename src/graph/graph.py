from graph.relationship import Relationship
from graph.node import Node


class Graph:

    def __init__(self, vector, nodes=None, relationships=None):
        if relationships is None:
            relationships = []
        if nodes is None:
            nodes = []
        self.vector = vector
        self.name = vector.name
        self.nodes = nodes
        self.relationships = relationships
        pass

    # Add the given node to this graph
    def add_node(self, node):
        self.nodes.append(node)

    # Add the given connector to this graph
    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    # Remove the node with the given node_id
    def remove_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                self.nodes.remove(node)

    # Remove the relationship with the given relationship_id
    def remove_relationship(self, relationship_id):
        for relationship in self.relationships:
            if relationship.id == relationship_id:
                self.relationships.remove(relationship)

    # Save a CSV representation of this graph at the specified path.
    def to_csv(self, path):
        pass

    # Save an image file of this graph at the specified path
    def to_image(self, file_type, path):
        if file_type == "png":
            pass
        if file_type == "jpeg":
            pass

    # commit the graph object
    def commit(self):
        pass
