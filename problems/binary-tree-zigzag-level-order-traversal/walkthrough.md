## The idea

A zigzag traversal reads the first level left to right, the second right to left, the third left to right, and so on. The hard-looking part is the direction flip, but it is not needed during the traversal. Walk every level left to right as in an ordinary level-order traversal, and simply reverse the list of values for every second level.

Keeping the walk fixed matters because the next level is built from the current one. If you reversed the nodes themselves, you would have to also flip the order you read their children. Reversing only the recorded values avoids that.

## Set-up

- `level` is the list of nodes on the current depth, always in left-to-right order. It starts as `[root]`.
- `reverse` says whether this level's output should be flipped. It starts `False` and toggles every level.
- `result` is the list of rows we return.

Invariant: at the top of each loop, `level` is the complete current depth, left to right.

```text
        3
       / \
      9   20
         /  \
        15   7

level = [3]      reverse = False      result = []
```

## Step by step

Each round turns `level` into a row of values, flips it if needed, and then builds the next `level` from the children of every node in order.

```text
Round 1   level = [3]          values = [3]
          reverse False        row [3]
          children, left to right: 9, 20

Round 2   level = [9, 20]      values = [9, 20]
          reverse True         row [20, 9]
          children: 9 has none, 20 gives 15, 7

Round 3   level = [15, 7]      values = [15, 7]
          reverse False        row [15, 7]
          children: none, so level = [] and the loop stops

result = [[3], [20, 9], [15, 7]]
```

Round 2 printed `[20, 9]`, yet `level` stayed `[9, 20]`. That is why round 3 saw `[15, 7]` and not `[7, 15]`.

## Why it works

Every level is processed in the same fixed order, so `level` is correct by induction: the children of a left-to-right list, taken left child then right child, are the next level left to right. The only difference between levels is the final reverse of a list of numbers.

## Where it goes wrong

Reversing `level` itself, instead of a copy of its values, scrambles the next level. Take round 2 above: if `level` became `[20, 9]`, the next level would be built from 20's children first, giving `[15, 7]` here only by luck of 9 having none. With a tree where 9 also had children, they would come out after 20's, and the rows below would no longer be left to right.

An empty tree must return `[]`, which the first `if` handles. Missing children are filtered out by `if child`.

## Cost

Time O(n): each node is visited once and each row is reversed at most once. Space O(n): the output holds every value, and `level` can hold a whole row (up to about n / 2 nodes).
