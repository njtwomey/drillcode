---
title: Level-by-level BFS
area: Trees
topics: [Tree]
problems:
  - binary-tree-level-order-traversal
  - binary-tree-right-side-view
related: [tree-recursion-return-and-best, bfs-shortest-paths]
---
## Reach for it when

- The statement says "level order", "each level", "by depth" or "zigzag".
- You need one value per level: right side view, left side view, the largest per row.
- You need minimum depth, or any answer that is the number of levels.

## Setup

- `queue = deque([root])`: the nodes of the current level, then of the next. Guard `root is None` first, because `deque([None])` crashes on `node.val`.
- `result = []`: one entry per level.
- `size = len(queue)` (or `range(len(queue))`), read before the inner loop: how many nodes belong to this level.
- Invariant: at the top of each `while queue` iteration, `queue` holds exactly one level.

## Template

```python
from collections import deque


def levels(root):
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

## What it removes

It removes sentinels and stored depths. Reading the length before the inner loop freezes the level size, so children appended inside the loop wait for the next pass. Every node is handled once, so the cost is O(n).

## Pitfalls

- Pushing `None` children. The next pop then reads `.val` on `None`. Test `if node.left` before appending.
- Reading `len(queue)` inside the loop condition, as in `while len(queue) > 0` for the inner loop. The queue grows as children are added and the levels merge. `range(len(queue))` is evaluated once, which is why it works.
- Using a list with `pop(0)`: it is O(n) per pop. Use `deque`.
- Empty tree: return `[]`, not `[[]]`.

## Variants

- `binary-tree-level-order-traversal`: collect each level's values into a list.
- `binary-tree-right-side-view`: keep only the last node of each level (`i == size - 1`). Keeping the first gives the left side view. The number of outer iterations is the depth.
- DFS alternative for the side view: the solution's `rightSideViewDFS` visits right before left and records the first node seen at each depth (`depth == len(result)`).

## Worked example

Problem: `binary-tree-level-order-traversal`

```python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # Guard: deque([None]) would crash on node.val.
        if root is None:
            return []
        result = []
        # BFS queue holds the nodes of the current level, then the next one.
        queue = deque([root])
        while queue:
            level = []
            # len(queue) is frozen at the level's size, so children appended inside
            # the loop wait for the next pass. Every node is handled once: O(n).
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
```

`queue` and `result` are the template's. `range(len(queue))` is the frozen level size. `level` collects the values of one level, and the two `if` lines push only real children.
