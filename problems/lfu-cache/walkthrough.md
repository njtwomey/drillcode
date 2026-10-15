## The idea

An LFU cache evicts the key used the fewest times, and among ties the one used least recently. Doing that with every operation in O(1) needs a structure where you can find the victim straight away, and update "how often" and "how recently" for any key without searching.

The trick is to group keys by their use count. For each count, keep the keys in the order they were last used. The victim is then the oldest key in the group with the lowest count, and bumping a key is just a move from one group to the next.

## Set-up

- `values[key]` is the stored value.
- `freq[key]` is how many times the key has been used.
- `buckets[f]` is an `OrderedDict` of the keys used exactly `f` times, oldest first. The dictionary values are unused (`None`); only the order matters. Moving a key into a bucket appends it at the recent end.
- `min_freq` is the lowest count that currently has a non-empty bucket. The victim is always `buckets[min_freq]`'s first key.

Invariants: every cached key is in exactly one bucket, matching `freq`; `min_freq` points at a non-empty bucket.

```text
capacity = 2

values   {}
freq     {}
buckets  {}
min_freq 0
```

## Step by step

A `get` or an update to an existing key calls `_touch`: it removes the key from bucket `f`, deletes the bucket if empty (moving `min_freq` up when that bucket was the minimum), and appends the key to bucket `f + 1`.

```text
put(1,1)   new key        buckets {1: [1]}                 min_freq 1

put(2,2)   new key        buckets {1: [1, 2]}              min_freq 1

get(1)     touch 1        1 leaves bucket 1, enters bucket 2
                          buckets {1: [2], 2: [1]}         min_freq 1
                          returns 1

put(3,3)   full! evict    min_freq 1, bucket 1 = [2], oldest is 2
                          evict 2, then insert 3 with count 1
                          buckets {1: [3], 2: [1]}         min_freq 1

get(2)     missing        returns -1

get(3)     touch 3        bucket 1 becomes empty and was the minimum
                          buckets {2: [1, 3]}              min_freq 2
                          returns 3

put(4,4)   full! evict    min_freq 2, bucket 2 = [1, 3], oldest is 1
                          evict 1, insert 4 with count 1
                          buckets {2: [3], 1: [4]}         min_freq 1

get(1)     missing        returns -1
get(3)     touch 3        buckets {1: [4], 3: [3]}         min_freq 1, returns 3
get(4)     touch 4        bucket 1 empties, was minimum
                          buckets {3: [3], 2: [4]}         min_freq 2, returns 4
```

The results, `1, -1, 3, -1, 3, 4`, are what the cache should produce. Bucket 2 at the eviction of key 1 shows the tiebreak: keys 1 and 3 both had count 2, and 1 was used earlier.

## Why it works

The bucket for each count keeps its keys in order of last use, because every move into a bucket appends at the end. So the front of the lowest non-empty bucket is exactly the least frequent, then least recent key. `min_freq` only needs care in two places. A new key has count 1, so `min_freq` is set to 1. A touch raises `min_freq` by one only if it just emptied the lowest bucket, because the touched key itself now sits in `f + 1`.

## Where it goes wrong

- Not counting `put` on an existing key as a use. It updates the value and calls `_touch`.
- Leaving `min_freq` stale after an eviction. The new key sets it to 1, which is always right, since count 1 is the lowest possible.
- Evicting before checking whether the key already exists. Updating a key in a full cache must not evict anyone.
- Capacity 0: `put` returns immediately, otherwise `min_freq` would index an empty bucket.
- Forgetting to delete empty buckets. `min_freq` would then point at a bucket with no keys.

## Cost

Every `get` and `put` is O(1): a few dictionary operations, with `OrderedDict` giving O(1) removal anywhere and `popitem(last=False)` for the oldest. Space O(capacity).
