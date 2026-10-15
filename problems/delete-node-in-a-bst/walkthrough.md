## The idea

In a binary search tree, everything in the left subtree is smaller than a node and everything in the right is larger. Finding a key is a walk: go left if smaller, right if larger. Deleting is the same walk, with a repair at the end.

The repair depends on how many children the doomed node has. Zero or one is easy: the child (or nothing) takes its place. Two children is the interesting case. You need a value that can sit at this position and keep the ordering intact. The inorder successor, the smallest value in the right subtree, is such a value: it is bigger than everything on the left and no bigger than anything else on the right.

## Set-up

`deleteNode(root, key)` returns the root of the subtree after deletion. The caller assigns that return value back into `root.left` or `root.right`, so any change in what sits in that slot is relinked automatically.

- `root is None`: the key is not in the tree, so return `None`.
- `key < root.val`: recurse left. `key > root.val`: recurse right.
- Equal: found it. Use one of the three repairs below.

## Step by step

Delete `3` from this tree:

```text
        5                      5
       / \                    / \
      3   6        ──▶       4   6
     / \   \                /     \
    2   4   7              2       7
```

Details at node `3`, which has two children:

```text
1. successor = root.right = 4. It has no left child, so the loop stops.

        3
       / \
      2   4  ◀── successor

2. root.val = 4 (the value is overwritten, the node stays)

        4
       / \
      2   4  ◀── now a duplicate

3. root.right = deleteNode(root.right, 4)
   that call finds 4 with no left child and returns its right (None)

        4
       /
      2
```

Back at `5`, `root.left` is reassigned to that subtree and `5` is returned.

## Why it works

Taking the smallest value from the right subtree keeps the BST rule at the replaced position. Everything to the left is smaller than any right value, and everything else on the right is at least as large as the minimum. The successor node, being the leftmost of its subtree, has no left child, so removing it is the easy case and the recursion ends fast.

## Where it goes wrong

Not using the return value. If you wrote `self.deleteNode(root.left, key)` without assigning it, the parent keeps pointing at the old node:

```text
5.left still points at the deleted node 3 instead of the repaired subtree
```

Another trap is the root itself being the key: returning the new subtree root from the function is what lets the top-level caller get a new root. A missing key or empty tree just returns what it was.

## Cost

Time O(h): one walk down to the key and at most one more walk down to find the successor. Space O(h) for the recursion; h is log n for a balanced tree and n for a chain.
