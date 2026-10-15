## The idea

A `get(key, timestamp)` asks for the value from the latest `set` at or before that time. Scanning every past write would be O(n) per query. But the problem promises that `set` calls for a key arrive with increasing timestamps. So if we just append each write to a list, that list is already sorted by time, and we can binary search it.

## Set-up

- `self.store` maps each key to a pair of parallel lists `(times, values)`.
- `times` holds that key's timestamps in increasing order; `values[i]` is the value written at `times[i]`. Invariant: `times` is sorted, because we only ever append larger timestamps.
- `set` appends to both lists. No sorting is needed.

```text
set("foo", "bar", 1)
set("foo", "bar2", 4)

store = { "foo": ( times  = [1,    4],
                   values = ["bar", "bar2"] ) }
```

## Step by step

`get` uses `bisect_right(times, timestamp)`, which returns how many stored timestamps are `<= timestamp`. The entry just before that position is the latest write not after the query.

```text
times = [1, 4]       values = ["bar", "bar2"]

get("foo", 3)    bisect_right([1,4], 3) = 1   -> values[0] = "bar"
                  index:  0  1
                  times: [1, 4]
                            ^ insertion point 1; take the item before it

get("foo", 4)    bisect_right([1,4], 4) = 2   -> values[1] = "bar2"
                  (an exact match counts, because it is right-biased)

get("foo", 0)    bisect_right([1,4], 0) = 0   -> nothing earlier, ""

get("zzz", 5)    key not in store             -> ""
```

## Why it works

`bisect_right` returns the position after all entries equal to or less than the query, so `idx - 1` is the last entry at or before the query. Sortedness is what makes binary search valid, and appending in increasing order maintains it for free. If `idx` is 0, every stored timestamp is later than the query, so there is no valid answer and the result is the empty string.

## Where it goes wrong

- Using `bisect_left`. It points before an exact match, so a query at timestamp 4 would return the previous value.

```text
times = [1, 4], query 4
bisect_right -> 2 -> values[1] = "bar2"   (correct)
bisect_left  -> 1 -> values[0] = "bar"    (stale; would need extra care)
```

- Not guarding `idx == 0`. `values[-1]` would silently return the LAST value instead of the empty string.
- Not handling a missing key, which would raise a `KeyError`.

## Cost

`set` is O(1) amortised. `get` is O(log n) in the number of writes to that key. Space O(n) for all writes.
