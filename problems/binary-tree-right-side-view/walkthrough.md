## The idea

Standing on the right of a tree, at each depth you see the rightmost node of that depth. Nodes on the left of a level are hidden by it, unless that level has nothing further right. So the answer is simply "the last node of each level".

That reduces to level-order traversal. Process the tree one level at a time, and record the value of the final node popped from each level.

## Set-up

- `queue` holds the current level, then the next one, starting with `root`. An empty tree returns `[]` immediately.
- `size = len(queue)` is taken at the start of each level, so the inner loop covers exactly that level.
- `i` is the position within the level. When `i == size - 1`, this is the last node of the level, and its value goes into `result`.
- Children are pushed left first, then right, so the rightmost node of a level always comes out last.

## Step by step

Tree `[1,2,3,4,null,null,null,5]`. The left side is deeper than the right:

```text
        1
       / \
      2   3
     /
    4
   /
  5
```

```text
Level 1  queue [1]        size 1
  i=0 pop 1  last? yes  result [1]     push 2, 3
Level 2  queue [2, 3]     size 2
  i=0 pop 2  last? no                  push 4
  i=1 pop 3  last? yes  result [1, 3]
Level 3  queue [4]        size 1
  i=0 pop 4  last? yes  result [1, 3, 4]   push 5
Level 4  queue [5]        size 1
  i=0 pop 5  last? yes  result [1, 3, 4, 5]
```

The view from the right is `[1, 3, 4, 5]`. The 4 and 5 are on the left branch, but with nothing to their right at those depths they are visible.

```text
depth 0:  1
depth 1:  2  [3]     3 hides 2
depth 2:  [4]        nothing on the right, so 4 shows
depth 3:  [5]
```

## Why it works

Within a level, nodes come out of the queue from left to right, so the last one popped is the rightmost at that depth. Each depth contributes exactly one entry, so `result` is ordered by depth.

## Where it goes wrong

Assuming the answer is just the right spine (`root.right.right...`). That fails whenever a left subtree is deeper than the right, as above. Also pick the last node of the level, not the last node pushed overall.

## Other approaches

The solution file also has `rightSideViewDFS`. It visits right before left and records a value only when `depth == len(result)`, meaning this is the first node reached at a new depth. Since the right child is visited first, the first node at each depth is the rightmost one.

```text
dfs(1,0): result [1]
  dfs(3,1): result [1, 3]
  dfs(2,1): depth 1 already has an entry
    dfs(4,2): result [1, 3, 4]
      dfs(5,3): result [1, 3, 4, 5]
```

It uses recursion depth instead of a queue.

## Cost

Time O(n): each node is visited once. Space O(n) for the queue (a wide level) or O(h) of stack for the DFS version.
