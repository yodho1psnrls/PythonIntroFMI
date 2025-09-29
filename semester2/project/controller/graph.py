

# Adjacency list (Forward edges only, Not Bidirectional)
class Graph:
    def __init__(
        self,
        nodes: list = [],
        adjacency: list[list[int]] = None
    ):
        self.nodes = nodes
        if adjacency is None:
            self.adj = [[]]*len(nodes)
        else:
            if len(adjacency) != len(nodes):
                raise ValueError("The number of rows in the connectivity matrix should match the length of nodes")
            self.adj = adjacency

    def node_count(self) -> int:
        return len(self.nodes)

    def edge_count(self) -> int:
        return sum([len(row) for row in self.adj])

    # the node degree (how many edges originate from it)
    def degree(self, node_id) -> int:
        return len(self.adj[node_id])

    __sizeof__ = node_count

    def add_node(self, node=None):
        self.nodes.append(node)
        self.adj.append([])
        # return len(self.nodes) - 1

    def add_edge(self, from_id: int, to_id: int):
        if not (self.is_valid_node(from_id) and self.is_valid_node(to_id)):
            raise IndexError("Invalid node ids to add edge between")
        self.adj[from_id].append(to_id)

    def pop_node(self, node_id: int):
        if not self.is_valid_node(node_id):
            raise IndexError("Invalid node_id to pop")
        self.nodes.pop(node_id)
        self.adj.pop(node_id)
        for row in self.adj:
            for ei in range(len(row)):
                if row[ei] == node_id:
                    row.pop(ei)
                else:
                    row[ei] -= int(node_id < row[ei])
        return self

    def pop_edge(self, from_id: int, to_id: int):
        if not self.is_valid_edge(from_id, to_id):
            raise IndexError("Invalid edge to pop")
        self.adj[from_id].remove(to_id)

    def adjacent_ids(self, node_id: int) -> list[int]:
        return self.adj[node_id]

    def adjacent(self, node_id: int) -> list[int]:
        return [self.nodes[i] for i in self.adj[node_id]]

    def is_valid_node(self, node_id: int) -> bool:
        return 0 <= node_id and node_id < len(self.nodes)

    def is_valid_edge(self, from_id, to_id) -> bool:
        return to_id in self.adj[from_id]

    def is_valid(self) -> bool:
        if len(self.nodes) != len(self.adj):
            return False
        for row in self.adj:
            for i in row:
                if not self.is_valid_node(i):
                    return False
        return True
