## The idea

A camera on a node watches the node itself, its parent and its children. You want the fewest cameras that watch every node. The key is where not to put them. A camera on a leaf watches only the leaf and its parent. The same camera on the leaf's parent watches the leaf, the parent and the grandparent, which is strictly more. So never put a camera on a leaf. Wait, and let the parent of any unwatched node take it.

That suggests deciding from the bottom up: each node looks at what its children report and decides whether it needs to be the camera.

## Set-up

Each call to `dfs(node)` returns one of three states for the node after its subtree is handled:

- `NEEDS` (0): not watched yet, so the parent must handle it.
- `COVERED` (1): watched by a child's camera, but holds no camera.
- `CAMERA` (2): holds a camera.

`cameras` counts the cameras placed so far. A missing child (`None`) returns `COVERED`: it has nothing to watch and does not force a camera above it.

The rules for a node, in order:

```text
child is NEEDS            ->  put a camera here, return CAMERA
else child is CAMERA      ->  return COVERED
else (all children COVERED) -> return NEEDS
```

## Step by step

Tree `[0, 0, null, 0, 0]`: root A, A's left child B, and B has two leaf children C and D.

```text
        A
       /
      B
     / \
    C   D
```

```text
dfs(C): both children None -> COVERED, COVERED  =>  return NEEDS
dfs(D): same                                     =>  return NEEDS
dfs(B): left is NEEDS  =>  cameras = 1,  return CAMERA
dfs(A): left = CAMERA, right (None) = COVERED   =>  return COVERED

Final:     A: COVERED
           B: CAMERA
          C   D: both watched by B
```

The root came back `COVERED`, so no extra camera is needed. The answer is `cameras = 1`.

## Why it works

Leaves always report `NEEDS`, which forces the camera onto their parent, the best place for it. A node that has a `CAMERA` child is already watched and can wait. Only when all children are merely `COVERED` does a node report `NEEDS`, passing the decision up one level, where a camera can again do the most good. This greedy choice never uses more cameras than any other plan, because moving a camera from a node to its parent never loses coverage of anything that mattered.

## Where it goes wrong

- Placing a camera on the leaf. For a chain of four nodes this gives 2 or more, but putting one on the second node from the bottom and one on the second from the top is also 2; on longer chains the leaf rule wastes cameras.
- Forgetting the root. It has no parent to cover it, so if `dfs(root)` returns `NEEDS` the code adds one more camera.
- Returning `NEEDS` for `None`. Then every leaf would force a camera onto a phantom child.

```text
Single node: dfs(root) -> NEEDS, nothing above it.
             cameras += 1  =>  answer 1
```

## Cost

Time O(n): each node is visited once. Space O(h) for the recursion stack, where h is the height of the tree.
