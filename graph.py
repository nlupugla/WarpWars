BLOCKED = 999999999

class Node:
    """
    A node connects to other nodes via Edges to form a graph

    Each node has a unique identifier (ID) so they can be mathematically distinct. Optionally, a node also has an x and
    y coordinate.
    """
    n_nodes = 0
    def __init__(self, x = 0, y = 0):
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

class Edge:
    """
    An edge is a connection between two nodes.

    Edges have a unique identifier and a list of two nodes. Optionally, an edge can have a numerical weight. Edges can
    also be directed, in which case it is only possible to traverse the edge in one direction, not both.
    """
    n_edges = 0
    def __init__(self, node1, node2, weight = 1, directed = False):
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
        self.nodes = [node1, node2]
        self.directed = directed

    def __eq__(self, other):
        return (self.ID, self.weight, self.nodes, self.directed) == (other.ID, other.weight, other.nodes, other.directed)

    def __hash__(self):
        return hash((self.ID, self.weight, self.nodes, self.directed))

class Graph:
    """
    A graph is a mathematical collection of nodes and edges.

    Graphs have a dictionary that maps each node in the graph to the set of edges connected to it. For now, we assume
    that the graph in question is connected. If you want something that handles a graph with disconnected components,
    ask nicely and maybe, maybe we'll get around to it.
    """

    def __init__(self, mapping = {}):
        """
        Create a new graph

        :param mapping: a mapping of nodes to their corresponding set of edges
        :return: an initialized Graph object
        """
        self.mapping = mapping # Key: node -> Item: edges

    def neighbourhood(self, node):
        """
        Return the set of nodes neighbouring the given one. Note that a node always neighbours itself.

        Note that a node always neighbours itself and that both nodes in a directed edge neighbour each other.
        :param node: a Node object
        :return: the set of all nodes neighboring the given node.
        """
        edges = self.mapping[node]
        neighbours = set([node])
        # collect list of neighbours
        for edge in edges:
            nodes = edge.nodes
            other_node = nodes[0] if node == nodes[0] else nodes[1]
            neighbours.add(other_node)
        return neighbours

    def are_neighbours(self, node1, node2):
        """
        Determine whether two nodes are neighbours.

        Note that a node always neighbours itself and that both nodes in a directed edge neighbour each other.
        :param node1: first node
        :param node2: second node
        :return: True if node1 neighbours node2, otherwise False.
        """
        return node1 in self.neighbourhood(node2)

    def connecting_edge(self, node1, node2):
        edges = self.mapping[node1]
        for edge in edges:
            if node2 in edge.nodes:
                return edge
        print "No connecting edge found, node1 and node2 are not neighbours."
        # TODO: actual error checking
        return False

    def best_path(self, start_node, end_node, path, unvisited_nodes=None, visited_nodes=None, visit_costs=None):
        """
        Calculate the least-cost path for getting from the start_node to the end_node using Dijkstra's algorithm.

        :param start_node: the node to traverse from.
        :param end_node: the node to traverse to.
        :param path: an ordered list of nodes constituting the solution when the algorithm finishes.
        :param unvisited_nodes: should always be None when called by user, it is used for recursion.
        :param visited_nodes: should always be None when called by user, it is used for recursion.
        :param visit_costs:  should always be None when called by user, it is used for recursion.
        :return: the numerical cost of traversing the calculated path.
        """
        # initialization
        if unvisited_nodes is None:
            if start_node == end_node:
                return 0
            unvisited_nodes = set(self.mapping.keys()) - set(start_node)
            visited_nodes = set(start_node)
            visit_costs = {}
            for node in self.mapping:
                visit_costs[node] = 0 if node == start_node else BLOCKED

        # find the set of unvisited neighbours
        unvisited_neighbours = set(self.neighbourhood(start_node)) & unvisited_nodes
        # update visit_costs
        for neighbour in unvisited_neighbours:
            new_visit_cost = visit_costs[start_node] + self.connecting_edge(start_node, neighbour).weight
            if new_visit_cost < visit_costs[neighbour]:
                visit_costs[neighbour] = new_visit_cost
        # update visited and unvisited nodes
        visited_nodes.add(unvisited_nodes.pop(start_node))
        # when the path reaches a dead-end or the end_node, return
        best_node = min(visit_costs, visit_costs.get)
        if visit_costs[best_node] >= BLOCKED:
            return visit_costs[best_node]
        path.append(best_node)
        if start_node == end_node:
            return visit_costs[best_node]
        unvisited_visit_costs = {}
        # otherwise, recurse using the least expensive unvisited node
        for node in unvisited_nodes:
            unvisited_visit_costs[node] = visit_costs[node]
        best_unvisited_node = min(unvisited_visit_costs, unvisited_visit_costs.get)
        return self.traversal_cost(self, best_unvisited_node, end_node, path, unvisited_nodes, visited_nodes, visit_costs)



    def are_connected(self, node1, node2, unvisited_nodes=None, visited_nodes=None):
        """
        Determine if two nodes are connected in the graph.

        :param node1: first node.
        :param node2: second node.
        :param unvisited_nodes: should always be None when called by user, it is used for recursion.
        :param visited_nodes: should always be None when called by user, it is used for recursion.
        :return: True when node1 is in the same connected component of the graph as node2, otherwise False.
        """
        # TODO: Test this, pretty sure it is super buggy
        if self.are_neighbours(node1, node2):
            return True
        if unvisited_nodes is None:
            unvisited_nodes = set(self.mapping.keys()) - set(node1)
            visited_nodes = set(node1)
        for neighbour in self.neighbourhood(node1):
            for second_neighbour in self.neighbourhood(neighbour):
                if second_neighbour in unvisited_nodes:
                    return self.are_connected(neighbour, node2, unvisited_nodes, visited_nodes)
            visited_nodes.add(unvisited_nodes.pop(neighbour))
        return False

