## The idea

Copying the whole array on every `snap` costs O(length) each time, and there can be tens of thousands of snaps. The array rarely changes between snaps, so store only the changes.

For each index keep a short list of `(snap_id, value)`: "from this snap on, the index held this value". To read index `i` at snapshot `s`, find the latest change recorded at or before `s`. The list is sorted by snap id, so that is a binary search.

## Set-up

- `self.snap_id` is the id the next snapshot will get. It is also "the current snap", used to tag new writes.
- `self.history[i]` is index `i`'s change list. It starts as `[(0, 0)]`, meaning "value 0 from snap 0", so every lookup finds something. Invariant: the snap ids in a list strictly increase.

```text
SnapshotArray(2)

 snap_id = 0
 history[0] = [(0, 0)]
 history[1] = [(0, 0)]
```

## Step by step

```text
set(0, 5)    last entry has snap 0 == snap_id, so overwrite it
   history[0] = [(0, 5)]

snap()       returns 0, snap_id becomes 1

set(0, 6)    last entry snap 0 != 1, so append
   history[0] = [(0, 5), (1, 6)]

snap()       returns 1, snap_id becomes 2

set(0, 7)    append
   history[0] = [(0, 5), (1, 6), (2, 7)]
   history[1] = [(0, 0)]
```

`snap` is O(1): it only bumps a counter. Now the reads, using `bisect_right` on the snap ids and then stepping back one:

```text
get(0, 0)  ids [0, 1, 2]  bisect_right(0) = 1  -> entry 0 -> 5
get(0, 1)  ids [0, 1, 2]  bisect_right(1) = 2  -> entry 1 -> 6
get(1, 1)  ids [0]        bisect_right(1) = 1  -> entry 0 -> 0
```

The last one shows an index that was never touched after snap 0: the search lands on its only entry.

## Why it works

An entry `(s, v)` is valid for every snapshot from `s` until the next entry. `bisect_right` gives the count of entries with id at most the query, so the one before that position is the latest entry that is not newer than the snapshot. Overwriting when `snap_id` has not moved means several sets before one snap keep only the last, which is the value the snapshot captures.

## Where it goes wrong

Using `bisect_left` breaks exact matches. For ids `[0, 1, 2]` and query 0, `bisect_left` returns 0, and `pos - 1` is -1, which reads the newest entry.

```text
get(0, 0), ids [0, 1, 2]
  bisect_left  = 0 -> changes[-1] -> 7   wrong (should be 5)
  bisect_right = 1 -> changes[0]  -> 5   right
```

Without the overwrite branch, two sets in the same snap would append two entries with the same id and the search could pick the first, older one.

## Cost

`set` and `snap` are O(1). `get` is O(log s), where `s` is the number of changes at that index. Space is O(length + number of sets).
