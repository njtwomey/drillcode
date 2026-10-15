## The idea

A single traversal of values cannot rebuild a tree, because many shapes give the same list. The fix is to also write down where the branches stop. Walk the tree in pre-order (node, then left subtree, then right subtree) and write a marker `#` for every missing child. Now the sequence has exactly one tree it can mean, and rebuilding is the same walk in reverse: read a token, and let the recursion consume exactly the tokens of its own subtree.

## Set-up

Serialize:

- `result` collects tokens.
- `stack` drives an iterative pre-order. It starts with `root`, which may be `None`. Right is pushed before left so that left is popped first.
- Tokens are joined with commas, so negative and multi-digit values stay intact.

Deserialize:

- `tokens` is a single shared iterator over the split string. It acts as a cursor that every call advances.
- `build()` reads the next token and returns a subtree.

```text
tree:       1
           / \
          2   3
             / \
            4   5

stack = [1]      result = []
```

## Step by step

```text
pop 1   write "1"; push 3 then 2        stack [3, 2]
pop 2   write "2"; push None, None      stack [3, N, N]
pop N   write "#"
pop N   write "#"                       stack [3]
pop 3   write "3"; push 5 then 4        stack [5, 4]
pop 4   write "4"; push None, None
pop N   "#"     pop N   "#"             stack [5]
pop 5   write "5"; push None, None
pop N   "#"     pop N   "#"

result: 1,2,#,#,3,4,#,#,5,#,#
```

Rebuilding reads the same string with `build()`:

```text
build -> 1
  left  build -> 2
    left  build -> #   None
    right build -> #   None
  right build -> 3
    left  build -> 4  (left #, right #)
    right build -> 5  (left #, right #)
```

Each call takes the next token from the shared iterator, so by the time `build` returns for node 2, the cursor sits at the `3`.

## Why it works

Pre-order lists the root first, so the first token is the root. A `#` marks an empty subtree, so the recursion knows when a branch ends without needing lengths. The left subtree must be built fully before the right, which matches the order the tokens were written.

## Where it goes wrong

- Without null markers the output is ambiguous: `1,2` could be a left or right child.
- Pushing left before right in the iterative serializer writes the right subtree first, and `deserialize` would mirror the tree.
- Joining without a delimiter merges `12` and `3` into one number.

## Cost

Time O(n) for both directions (2n + 1 tokens). Space O(n) for the string and the stack or recursion. The recursion in `deserialize` is as deep as the tree, which is fine for the 10^4 node limit but could be tall on a skewed tree.
