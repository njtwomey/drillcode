def validate(result, case, scaffolds):
    tree = scaffolds.tree
    Codec = case["entry"]
    root = case["args"]["root"]
    expected = tree.tree_to_array(tree.build_tree(case["input"]["root"]))
    data = Codec().serialize(root)
    if not isinstance(data, str):
        return False, f"serialize must return a string, got {type(data).__name__}"
    rebuilt = Codec().deserialize(data)
    actual = tree.tree_to_array(rebuilt)
    if actual != expected:
        return False, f"round trip gave {actual}, expected {expected}"
    if rebuilt is not None and rebuilt is root:
        return False, "deserialize returned the original object"
    return True, ""
