def validate(result, case, scaffolds):
    original = scaffolds.tree.build_tree(case["input"]["root"])
    key = case["input"]["key"]

    # Values that must remain: everything originally present except key.
    expected = []
    stack = [original]
    while stack:
        node = stack.pop()
        if node is not None:
            if node.val != key:
                expected.append(node.val)
            stack.extend((node.left, node.right))
    expected.sort()

    # Inorder walk of the result, bounded so a cyclic structure cannot hang us.
    values = []
    stack = []
    curr = result
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
            if len(stack) > len(expected) + 1:
                return False, "result has more nodes than expected (or a cycle)"
        curr = stack.pop()
        values.append(curr.val)
        if len(values) > len(expected):
            return False, "result has more nodes than expected"
        curr = curr.right

    if values != expected:
        return False, f"inorder values are {values}, expected sorted {expected}"
    return True, ""
