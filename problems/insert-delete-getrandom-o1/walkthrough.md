## The idea

Three operations must all be O(1). A hash map gives O(1) insert, delete and membership, but you cannot pick a random key from it in O(1). A list gives O(1) random pick by index, but deleting from the middle is O(n) because everything shifts.

Use both. The list holds the values, so `getRandom` is a random index. The dict maps each value to its index in the list, so we can find a value in O(1). The only problem left is deleting from the middle of the list, and there is a neat fix: swap the doomed element with the last one, then pop the tail. Order in the list does not matter, so this costs O(1).

## Set-up

- `self.values` is the list of members. Invariant: it holds each member exactly once, in any order.
- `self.pos` maps a member to its index in `values`. Invariant: `values[pos[v]] == v` for every member `v`.

```text
insert 1, 2, 3, 4

 values: [1, 2, 3, 4]
 index :  0  1  2  3

 pos:  1->0   2->1   3->2   4->3
```

## Step by step

`remove(2)`. We read `idx = 1` and `last = 4`.

```text
step 1  values[idx] = last      [1, 4, 3, 4]
                                    ^idx  ^ old tail
step 2  pos[last] = idx         pos: 1->0  2->1  3->2  4->1
step 3  values.pop()            [1, 4, 3]
step 4  del pos[val]            pos: 1->0  3->2  4->1
```

The hole at index 1 is filled by the old tail, and the invariant holds again. Nothing shifted.

Now `remove(3)` on `[1, 4, 3]`, where the target is the last element itself:

```text
idx = 2, last = 3
values[2] = 3          [1, 4, 3]     (no change)
pos[3] = 2             (no change)
values.pop()           [1, 4]
del pos[3]             pos: 1->0  4->1
```

`insert` is simple: if `val` is in `pos` return `False`, otherwise record its index and append.

## Why it works

Each operation preserves "`values` holds the members once, and `pos` says where". Insert appends at the end and records that end index. Remove overwrites one slot with a member that is moved, updates that member's index, and drops the tail. `getRandom` picks a uniform index of a list with no duplicates, so every member is equally likely.

## Where it goes wrong

The order of `pos[last] = idx` and `del pos[val]` matters when `val` is itself the last element. Then `last == val`, so the update writes `val` back into `pos`. If you deleted first and updated second, the stale entry would survive:

```text
remove(3) with the delete done before the update:
  del pos[3]            pos: 1->0  4->1
  pos[3] = 2            pos: 1->0  4->1  3->2   <- 3 is back in pos
```

Later `insert(3)` would return `False`, and the set would think it still contains 3. Updating first and deleting last avoids this.

## Cost

Every operation is O(1) on average: dict lookups and list append, pop and index. Space is O(n) for the list and the dict.
