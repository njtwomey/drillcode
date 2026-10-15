def _nodes(head):
    out = []
    seen = set()
    while head is not None and id(head) not in seen:
        seen.add(id(head))
        out.append(head)
        head = head.next
    return out


def validate(result, case, scaffolds):
    original = case["args"]["head"]
    expected = case["expected"]
    if not expected:
        return (result is None, "expected None for an empty list")
    if result is None:
        return False, "returned None for a non-empty list"
    if scaffolds.linked_list.random_list_to_array(result) != expected:
        return False, "copied list structure (values, next, random) differs from the original"
    originals = {id(n) for n in _nodes(original)}
    # random pointers may also reference nodes outside the next-chain if the copy is wrong
    for node in _nodes(result):
        if id(node) in originals:
            return False, "result reuses an original node instead of copying it"
        if node.random is not None and id(node.random) in originals:
            return False, "a random pointer in the result points into the original list"
    return True, ""
