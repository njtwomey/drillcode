class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_graph(adjacency):
    """adjacency[i] lists the neighbour values of the node with value i + 1."""
    if not adjacency:
        return None
    nodes = [Node(i + 1) for i in range(len(adjacency))]
    for i, neighbours in enumerate(adjacency):
        nodes[i].neighbors = [nodes[v - 1] for v in neighbours]
    return nodes[0]


def graph_to_adjacency(node):
    """Inverse of build_graph, for the nodes reachable from node."""
    if node is None:
        return []
    seen = {id(node): node}
    queue = [node]
    head = 0
    while head < len(queue):
        current = queue[head]
        head += 1
        for neighbour in current.neighbors:
            if id(neighbour) not in seen:
                seen[id(neighbour)] = neighbour
                queue.append(neighbour)
    ordered = sorted(seen.values(), key=lambda n: n.val)
    return [[n.val for n in current.neighbors] for current in ordered]
