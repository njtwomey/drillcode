def validate(result, case, scaffolds):
    nums = case["input"]["nums"]
    values = []

    # Returns the subtree height, or -1 if some node's subtrees differ in height by more
    # than one. Appends values in inorder; a BST's inorder is sorted.
    def walk(node):
        if node is None:
            return 0
        if len(values) > len(nums):
            return -1
        left = walk(node.left)
        values.append(node.val)
        right = walk(node.right)
        if left < 0 or right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    if walk(result) < 0:
        return False, "tree is not height balanced"
    if values != nums:
        return False, f"inorder traversal is {values}, expected {nums}"
    return True, ""
