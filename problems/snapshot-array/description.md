Implement a class `SnapshotArray` that supports taking snapshots of an integer array.

`SnapshotArray(length)` creates an array of the given `length` with every element initially `0`. `set(index, val)` changes the element at `index`. `snap()` takes a snapshot of the whole array and returns the snapshot id, which is the number of earlier `snap` calls (the first snapshot has id `0`). `get(index, snap_id)` returns the value that `index` held when snapshot `snap_id` was taken, regardless of later changes.

Only snapshot ids that have already been returned are queried.

Constraints:
- `1 <= length <= 5 * 10^4`
- `0 <= val <= 10^9`
- At most `5 * 10^4` calls in total; copying the whole array on each `snap` is too slow
