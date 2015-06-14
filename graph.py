from node import Node
from edge import Edge
from constants import BLOCKED

class Graph:
    """
    A graph is a mathematical collection of nodes and edges.

    Graphs have a dictionary that maps each node in the graph to the set of edges connected to it. For now, we assume
    that the graph in question is connected. If you want something that handles a graph with disconnected components,
    ask nicely and maybe, maybe we'll get around to it.
    """

    def __init__(self):
        """
        Create a new graph.

        :return: an initialized Graph object
        """
        self.mapping = {} # Key: node -> Item: edges

    def copy(self):
        """
        Return a copy of the graph.

        :return: a new graph with the same values as the caller.
        """
        graph = Graph()
        for node in self.mapping:
            copy_of_node = node.copy()
            graph.add_node(copy_of_node)
            for other_node in self.mapping:
                edge = self.find_edge(node, other_node)
                if edge is not None:
                    copy_of_other_node = graph.find_node_by_ID(other_node.ID)
                    if copy_of_other_node is not None:
                        graph.connect(copy_of_node, copy_of_other_node, edge.weight, edge.directed)
        return graph

    def add_node(self, node):
        """
        Add a node to the graph.

        :param node: the node to add.
        :return: False if the graph already has node, otherwise True.
        """
        if self.mapping.has_key(node):
            return False
        self.mapping[node] = set()
        return True

    def add_new_node(self, x=0, y=0):
        """
        Create a new node and insert it into the graph at the position specified.

        :param x: x coordinate
        :param y: y coordinate
        :return: nothing.
        """
        node = Node(x, y)
        self.add_node(node)

    def find_node_by_ID(self, ID):
        """
        Return the node in the graph who's ID matches the input.

        :param ID: unique numerical identifier of the node to find.
        :return: the node in the graph with the ID specified.
        """
        for node in self.mapping:
            if node.ID == ID:
                return node

    def find_node_by_position(self, x, y):
        """
        Return the node in the graph who's position matches the input.

        :param x: x coordinate of position
        :param y: y coordinate of position
        :return: a node in the graph with the position specified. If many nodes in the graph have the position
        specified, which one of those this method returns is undefined.
        """
        for node in self.mapping:
            if node.x == x and node.y == y:
                return node

    def get_nodes(self):
        """
        Return all nodes in the graph.

        :return: a frozenset of all nodes in the graph.
        """
        return frozenset(self.mapping.keys())

    def num_nodes(self):
        """
        Return the number of nodes in the graph.

        :return: the number of nodes in the graph.
        """
        return len(self.get_nodes())

    def connect(self, node1, node2, weight=1, directed=False):
        """
        Add an edge to the graph that connects node1 to node2 if they are not already connected.

        :param node1: the first node.
        :param node2: the second node.
        :param weight: numerical weight of the new edge.
        :param directed: when True, the edge will be directed from node1 to node2.
        :return: False if node1 is already connected to node2, otherwise True.
        """
        if self.are_neighbours(node1, node2):
            return False
        edge = Edge(node1, node2, weight, directed)
        self.mapping[node1].add(edge)
        self.mapping[node2].add(edge)
        return True

    def connect_positions(self, position1, position2, weight=1, directed=False):
        """
        Add an edge to the graph that connects position1 with position2 if they are not already connected.

        This method will not connect two nodes that are already connected to each other. Note that if more than one node
        lives at either position, the specific node chosen from that group for the for the connection is undefined.
        :param position1: a 2-tuple of the form (x, y) that specifies the position of the first node.
        :param position2: a 2-tuple of the form (x, y) that specifies the position of the second node.
        :param weight: numerical weight of the new edge.
        :param directed: when True, the edge will be directed from position1 to position2.
        :return: False if position1 is already connected to position2, otherwise True.
        """
        node1 = self.find_node_by_position(position1[0], position1[1])
        node2 = self.find_node_by_position(position2[0], position2[1])
        return self.connect(node1, node2, weight, directed)

    def connect_adjacent_nodes(self):
        """
        Connect all nodes geometrically adjacent to each other in the graph.

        This method will not connect two nodes that are already connected to each other. Nodes are considered adjacent
        when the vector between them is (+/-1, 0) or (0, +/-1). For example, nodes at positions (2,3) and (3, 3) are
        adjacent to each other but nodes at (2,3) and (3,4) are not. A node is not adjacent to itself.
        :return: nothing.
        """
        for node in self.mapping:
            north_node = self.find_node_by_position(node.x, node.y + 1)
            east_node = self.find_node_by_position(node.x + 1, node.y)
            south_node = self.find_node_by_position(node.x, node.y - 1)
            west_node = self.find_node_by_position(node.x - 1, node.y)
            if north_node is not None:
                self.connect(node, north_node)
            if east_node is not None:
                self.connect(node, east_node)
            if south_node is not None:
                self.connect(node, south_node)
            if west_node is not None:
                self.connect(node, west_node)

    def connect_all_to(self, center_node):
        """
        Connect all nodes in the graph except the argument to the input node.

        :param center_node: the central node to witch all other nodes will connect.
        :return: nothing.
        """
        for other_node in self.mapping:
            if center_node != other_node:
                self.connect(center_node, other_node)

    def find_edge(self, node1, node2):
        """
        Return the edge connecting node1 to node2.

        :param node1: the first node.
        :param node2: the second node.
        :return: the edge connecting node1 to node2.
        """
        for edge in self.mapping[node1]:
            if node2 in edge.nodes:
                return edge

    def edit_edge(self, edge, weight, directed=False):
        """
        Assign a new weight and directedness to an edge.

        :param edge: the edge to edit.
        :param weight: new numerical weight of the edge.
        :param directed: new boolean directedness of the edge.
        :return: nothing.
        """
        edge.weight = weight
        edge.directed = directed

    def edit_connection(self, node1, node2, weight, directed=False):
        """
        Assign a new weight and directedness to the edge connecting node1 to node2.

        :param node1: the first node.
        :param node2: the second node.
        :param weight: new numerical weight of the connecting edge.
        :param directed: new boolean directedness of the edge.
        :return: False if there is no edge between node1 and node2, otherwise True.
        """
        if not self.are_neighbours(node1, node2):
            return False
        edge = self.find_edge(node1, node2)
        self.edit_edge(weight, directed)
        return True

    def block_node(self, node):
        """
        Block a node off from the rest of the graph by editing the weight of all connecting edges to be BLOCKED.

        :param node: the node to block.
        :return: nothing.
        """
        for edge in self.mapping[node]:
            self.edit_edge(edge, BLOCKED)

    def block_position(self, x, y):
        """
        Block a node at the specified position from the rest of the graph.

        :param x: x coordinate of the node to block.
        :param y: y coordinate of the node to block.
        :return: nothing.
        """
        self.block_node(self.find_node_by_position(x, y))

    def get_edges(self):
        """
        Return all edges in the graph.

        :return: the a frozenset of all edges in the graph.
        """
        edge_set = set()
        for node in self.mapping:
            edges = self.mapping[node]
            edge_set |= edges
        return frozenset(edge_set)

    def num_edges(self):
        """
        Return the number of edges in the graph.

        :return: the number of edges in the graph.
        """
        return len(self.get_edges())

    def neighbourhood(self, node):
        """
        Return the set of nodes neighbouring the given one.

        Note that a node always neighbours itself and that both nodes in a directed edge neighbour each other.
        :param node: a Node object
        :return: the set of all nodes neighboring the given node.
        """
        connected_edges = self.mapping[node]
        neighbours = set([node])  # a node always neighbours itself
        for edge in connected_edges:
            neighbours |= edge.nodes
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

    def traversal_cost(self, start_node, end_node, unvisited_nodes=None, visited_nodes=None, visit_costs=None):
        """
        Calculate the minimum traversal cost from start_node to end_node using Dijkstra's algorithm.

        :param start_node: the node to traverse from.
        :param end_node: the node to traverse to.
        :param unvisited_nodes: should always be None when called by user, it is used for recursion.
        :param visited_nodes: should always be None when called by user, it is used for recursion.
        :param visit_costs:  should always be None when called by user, it is used for recursion.
        :return: If start_node can access end_node, return the minimum traversal cost, otherwise return BLOCKED.
        """
        # initialization
        if unvisited_nodes is None:
            if start_node == end_node:
                return 0
            unvisited_nodes = set(self.mapping.keys())
            visited_nodes = set()
            visit_costs = {}
            for node in self.mapping:
                visit_costs[node] = 0 if node == start_node else BLOCKED

        # Find the set of unvisited neighbours.
        unvisited_neighbours = set(self.neighbourhood(start_node)) & unvisited_nodes
        # Compute visit_costs for the current node's neighbours.
        for neighbour in unvisited_neighbours:
            new_visit_cost = visit_costs[start_node] + self.find_edge(start_node, neighbour).weight
            if new_visit_cost < visit_costs[neighbour]:
                visit_costs[neighbour] = new_visit_cost
        # Mark the current node as visited.
        unvisited_nodes.remove(start_node)
        visited_nodes.add(start_node)
        # If end_node has been visited, terminate, the destination has been reached.
        if start_node == end_node:
            return visit_costs[start_node]
        # Otherwise, find the least costly unvisited node.
        unvisited_visit_costs = {}
        for node in unvisited_nodes:
            unvisited_visit_costs[node] = visit_costs[node]
        best_unvisited_node = min(unvisited_visit_costs, key=unvisited_visit_costs.get)
        # If that node is BLOCKED, terminate; the destination is inaccessible.
        if unvisited_visit_costs[best_unvisited_node] >= BLOCKED:
            return BLOCKED
        # Otherwise, recurse using the least costly unvisited node as the new start_node.
        return self.traversal_cost(best_unvisited_node, end_node, unvisited_nodes, visited_nodes, visit_costs)

    def generate_dict(self):
        # TODO: This is not ready yet
        nodes = []
        for node in self.mapping:
            nodes.append(node.generate_dict())
        # get only one instance of each edge
        edge_set = set()
        for node in self.mapping:
            for edge in self.mapping[node]:
                edge_set.add(edge)
        edges = []
        # now turn each of those into a dictionary
        for edge in edge_set:
            edges.append(edge.generate_dict())
        dictionary = {
            'nodes': nodes,
            'edges': edges
        }
        return dictionary


