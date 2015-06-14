from node import Node

class Edge:
    """
    An edge is a connection between two nodes.

    Edges have a unique identifier and a list of two nodes. Optionally, an edge can have a numerical weight. Edges can
    also be directed, in which case it is only possible to traverse the edge in one direction, not both.
    """
    n_edges = 0
    def __init__(self, node1, node2, weight=1, directed=False):
        """
        Create an edge with its own unique identifier

        :param node1: node at first end of the edge
        :param node2: node at second end of the edge
        :param weight: numerical weight of the connection between node1 and node2
        :param directed: if True, the edge is oriented from node1 to node 2
        :return: an initialized Edge object
        """
        Edge.n_edges += 1
        self.ID = Edge.n_edges
        self.weight = weight
        self.nodes = frozenset([node1, node2])
        self.directed = directed

    def __eq__(self, other):
        return (self.ID, self.weight, self.nodes, self.directed) == (other.ID, other.weight, other.nodes, other.directed)

    def __hash__(self):
        return hash(self.ID)

    def copy(self):
        nodes = []
        for node in self.nodes:
            nodes.append(node.copy())
        return Edge(nodes[0], nodes[1], self.weight, self.directed)

    def generate_dict(self):
        nodes = []
        for node in self.nodes:
            nodes.append(node.generate_dict())
        dictionary = {
            'ID': self.ID,
            'weight': self.weight,
            'nodes': nodes,
            'directed': self.directed
        }
        return dictionary
