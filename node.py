class Node:
    """
    A node connects to other nodes via Edges to form a graph

    Each node has a unique identifier (ID) so they can be mathematically distinct. Optionally, a node also has an x and
    y coordinate.
    """
    n_nodes = 0
    def __init__(self, x=0, y=0):
        """
        Create a node with its own unique identifier.

        :param x: x coordinate
        :param y: y coordinate
        :return: an initialized Node object
        """
        Node.n_nodes += 1
        self.ID = Node.n_nodes
        self.x = x  # x position
        self.y = x  # y position

    def __eq__(self, other):
        return (self.ID, self.x, self.y) == (other.ID, other.x, other.y)

    def __hash__(self):
        return hash((self.ID, self.x, self.y))

    def generate_dict(self):
        dictionary = {
            'ID': self.ID,
            'x': self.x,
            'y': self.y
        }
        return dictionary
