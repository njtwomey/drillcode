class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(level_order):
    """LeetCode level-order format: null marks a missing child."""
    if not level_order or level_order[0] is None:
        return None
    root = TreeNode(level_order[0])
    queue = [root]
    i = 1
    head = 0
    while head < len(queue) and i < len(level_order):
        node = queue[head]
        head += 1
        if i < len(level_order) and level_order[i] is not None:
            node.left = TreeNode(level_order[i])
            queue.append(node.left)
        i += 1
        if i < len(level_order) and level_order[i] is not None:
            node.right = TreeNode(level_order[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    """Inverse of build_tree, with trailing nulls trimmed."""
    if root is None:
        return []
    array = []
    queue = [root]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node is None:
            array.append(None)
        else:
            array.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while array and array[-1] is None:
        array.pop()
    return array


def find_node(root, val):
    """First node with this value in level order, or None."""
    queue = [root]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node is None:
            continue
        if node.val == val:
            return node
        queue.append(node.left)
        queue.append(node.right)
    return None
