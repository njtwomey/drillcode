def _reachable(node):
    seen = {}
    stack = [node]
    while stack:
        current = stack.pop()
        if current is None or id(current) in seen:
            continue
        seen[id(current)] = current
        stack.extend(current.neighbors)
    return seen


def validate(result, case, scaffolds):
    original = case["args"]["node"]
    expected = case["expected"]
    if not expected:
        return (result is None, "expected None for null input")
    if result is None:
        return False, "returned None for a non-empty graph"
    if scaffolds.graph.graph_to_adjacency(result) != expected:
        return False, "cloned graph structure differs from the original"
    shared = set(_reachable(result)) & set(_reachable(original))
    if shared:
        return False, f"{len(shared)} node(s) of the result are the original nodes, not copies"
    return True, ""
