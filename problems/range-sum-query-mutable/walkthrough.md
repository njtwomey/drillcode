## The idea

A plain prefix-sum array answers range sums in O(1) but an update forces you to rewrite everything after it, O(n). A plain array updates in O(1) but sums in O(n). A Fenwick tree (binary indexed tree) splits the difference: both operations cost O(log n).

It stores sums of blocks of different sizes, chosen so that any prefix is the sum of a few disjoint blocks, and any single element lives in only a few blocks. The block sizes come from binary: `i & -i`, the lowest set bit of `i`.

## Set-up

- `nums` is a copy of the current values, used to find how much an update changes.
- `tree` is 1-based with `n + 1` slots. `tree[i]` is the sum of the last `i & -i` elements ending at position `i`.
- Position `p` in the tree is index `p - 1` in `nums`.

```text
nums  : [1, 3, 5, 7, 9, 11]        positions 1..6

pos  binary  lowbit  covers (positions)   tree[pos]
 1    001      1     1                     1
 2    010      2     1..2                  1+3     = 4
 3    011      1     3                     5
 4    100      4     1..4                  1+3+5+7 = 16
 5    101      1     5                     9
 6    110      2     5..6                  9+11    = 20

tree = [_, 1, 4, 5, 16, 9, 20]
```

The build pushes each finished `tree[i]` into its parent `i + (i & -i)`, which is the next larger block that includes it. That is O(n) overall.

## Step by step

Update `nums[2]` from 5 to 10. `delta = 5`, start at position `i = 3` and add the lowest bit each time.

```text
i=3 (011)  tree[3]  5 -> 10     i += 1 -> 4
i=4 (100)  tree[4] 16 -> 21     i += 4 -> 8, past n=6, stop

tree = [_, 1, 4, 10, 21, 9, 20]
```

Query `sumRange(1, 4)` is `_prefix(5) - _prefix(1)`. A prefix subtracts the lowest bit to hop to the block before.

```text
_prefix(5):  k=5 (101) add tree[5] = 9    k -> 4
             k=4 (100) add tree[4] = 21   k -> 0     total 30
_prefix(1):  k=1 (001) add tree[1] = 1    k -> 0     total 1

30 - 1 = 29   (check: 3 + 10 + 7 + 9)
```

## Why it works

The prefix hops split `k` into its set bits: 5 = 4 + 1, so the blocks are the ones covering 1..4 and 5..5, which are disjoint and complete. For updates, `i + (i & -i)` visits exactly the blocks that contain position `i`, and each such step moves to a block at least twice as long, so there are at most log n of them.

## Where it goes wrong

- Mixing 0-based and 1-based indexes. The tree must start at position 1 (position 0 would have lowbit 0 and loop forever). That is why `update` starts at `index + 1` and the prefix takes `right + 1`.
- Adding the new value instead of the difference. The blocks already include the old value, so the update must add `val - self.nums[index]`.
- Using `_prefix(left)` for the lower bound but `_prefix(right)` for the upper, which drops `nums[right]`.

## Cost

Build O(n). Each `update` and `sumRange` touches at most about log2(n) blocks: O(log n). Space O(n) for `tree` and the copy of `nums`.
