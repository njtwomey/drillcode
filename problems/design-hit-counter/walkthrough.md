## The idea

We want the number of hits in the last 300 seconds. Because calls arrive in time order, hits are stored oldest first, and the old ones are always at the front. A hit that is too old for this query is too old for every later query too, so it can be thrown away for good.

A deque is the right container: append new hits on the right in O(1), remove expired hits from the left in O(1). The answer is the length of what remains.

## Set-up

- `self.window` is a deque of hit timestamps, oldest on the left. Invariant: it is sorted non-decreasing, since calls never go back in time. Repeated timestamps are kept as separate entries, one per hit.

```text
window = deque([])
```

## Step by step

`getHits(t)` counts hits in `[t - 299, t]`, so a hit is expired when `window[0] <= t - 300`.

```text
hit(1), hit(2), hit(3)         window: [1, 2, 3]

getHits(4)    cutoff = 4 - 300 = -296
              1 <= -296 ? no, stop              window: [1, 2, 3]
              returns 3

hit(300)                       window: [1, 2, 3, 300]

getHits(300)  cutoff = 0
              1 <= 0 ? no, stop                 window: [1, 2, 3, 300]
              returns 4

getHits(301)  cutoff = 1
              1 <= 1 ? yes, popleft             window: [2, 3, 300]
              2 <= 1 ? no, stop
              returns 3
```

The hit at second 1 is gone at 301 because the window `[2, 301]` no longer contains it.

## Why it works

Since the deque is sorted, the first hit that is still in range means every later one is in range as well, so the loop can stop at the first survivor. Everything removed is older than any future query can reach, because future timestamps are at least as large.

## Where it goes wrong

The boundary is easy to get off by one. The window has 300 seconds in it, `t - 299` through `t`, so a hit at exactly `t - 300` is outside.

```text
hit at 1, query at 301:
  window [t-299 .. t] = [2 .. 301]
  `<= t - 300`  evicts 1   -> count excludes it   right
  `<  t - 300`  keeps 1    -> count includes it   wrong
```

## Cost

`hit` is O(1). `getHits` is O(1) amortised, since each timestamp is added once and removed at most once. Space is O(hits within the window). For huge traffic you could store `(second, count)` pairs, or a circular array of 300 buckets, to bound memory.
