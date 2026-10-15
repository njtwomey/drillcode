"""uv run python scripts/gen_skeletons.py [slug ...]  -- regenerate skeleton.py from solution.py + tests.yaml."""

import ast
import sys

from _common import PROBLEMS, load_spec, problem_dirs

DEFINITIONS = {
    "ListNode": '''# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
''',
    "RandomNode": '''# Definition for a Node with a random pointer.
# class Node:
#     def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
#         self.val = int(x)
#         self.next = next
#         self.random = random
''',
    "TreeNode": '''# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
''',
    "GraphNode": '''# Definition for a Node.
# class Node:
#     def __init__(self, val=0, neighbors=None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []
''',
}


def definitions(spec):
    blocks = []
    convert = " ".join(str(v) for v in (spec.get("convert") or {}).values())
    for scaffold in spec.get("scaffolds", []):
        if scaffold == "linked_list":
            blocks.append(DEFINITIONS["RandomNode" if "random_list" in convert else "ListNode"])
        elif scaffold == "tree":
            blocks.append(DEFINITIONS["TreeNode"])
        elif scaffold == "graph":
            blocks.append(DEFINITIONS["GraphNode"])
    return "".join(blocks)


def skeleton(spec, source):
    entry = spec["entry"]
    cls_name, _, method = entry.partition(".")
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls_name)
    keep = []
    for node in cls.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        wanted = node.name == method if method else (node.name == "__init__" or not node.name.startswith("_"))
        if wanted:
            node.body = [ast.Pass()]
            node.decorator_list = []
            keep.append(node)
    cls.body = keep or [ast.Pass()]
    cls.decorator_list = []
    return definitions(spec) + ast.unparse(ast.fix_missing_locations(cls)) + "\n"


def main():
    for slug in sys.argv[1:] or problem_dirs():
        directory = PROBLEMS / slug
        spec = load_spec(slug)
        (directory / "skeleton.py").write_text(skeleton(spec, (directory / "solution.py").read_text()))


if __name__ == "__main__":
    main()
