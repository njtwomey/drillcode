## The idea

To find the `k` most common values you could count them and sort by count, which is O(n log n). A heap of size `k` gives O(n log k). There is something quicker, because a count is a small bounded integer: a value can appear at most `n` times. So instead of sorting counts, use them as indices into an array, a bucket sort. Put each value in the bucket labelled with its count, then read the buckets from the highest label down until you have `k` values.

## Set-up

- `Counter(nums)` gives each value's frequency.
- `buckets` has `len(nums) + 1` lists, so index `c` holds the values that appear exactly `c` times. Invariant: each distinct value sits in exactly one bucket.
- `result` collects values as we read buckets from the top.

```text
nums = [1, 1, 1, 2, 2, 3]    k = 2

counts: 1 -> 3,  2 -> 2,  3 -> 1

index:    0    1     2     3    4    5    6
buckets: [ ] [ [3] ] [ [2] ] [ [1] ] [ ] [ ] [ ]
```

## Step by step

Walk `count` from `len(nums)` (6) down to 1 and take everything found.

```text
count 6, 5, 4   empty buckets, nothing taken
count 3         bucket [1]   result = [1]        len 1, need 2
count 2         bucket [2]   result = [1, 2]     len == k, return
```

The scan stops early, so the bucket for count 1 (value 3) is never read. The answer is `[1, 2]`.

## Why it works

Reading from the high end down visits values in order of decreasing frequency, so the first `k` collected are the `k` most frequent. Work stays linear: building the buckets is O(n), and the scan covers `n` bucket slots and each value at most once.

## Where it goes wrong

- Making `buckets` too short. Counts reach `len(nums)` (all elements equal), so the array needs `n + 1` slots, since index 0 is unused.

```text
nums = [7, 7, 7]    n = 3    buckets needs indexes 0..3
count of 7 is 3 -> buckets[3]; a list of length 3 would fail here.
```

- Not stopping at `k`. If several values share a bucket, the check `len(result) == k` has to be inside the inner loop.
- Assuming a particular order within the result. The problem allows any order, and values in the same bucket come out in the order they were counted.

## Other approaches

A min-heap of size `k` over `(count, value)` pairs works in O(n log k) and uses less memory when `k` is much smaller than the number of distinct values. `Counter.most_common(k)` does the same thing in one call.

## Cost

Time O(n): counting, building, and scanning the buckets are each linear. Space O(n) for the counter and buckets.
