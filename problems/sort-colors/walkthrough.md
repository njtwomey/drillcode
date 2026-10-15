## The idea

There are only three values: 0, 1 and 2. A general sort is overkill, and counting 0s, 1s and 2s then rewriting needs two passes. The Dutch national flag method does it in one pass by keeping the array in four zones and sweeping a single pointer through the unexamined one: 0s are tossed to the front, 2s to the back, and 1s are left in the middle.

## Set-up

Three indices carve the array into zones.

- `lo` is where the next 0 should land. Everything before it is a settled 0.
- `mid` is the cell being examined. Everything from `lo` to `mid - 1` is a settled 1.
- `hi` is where the next 2 should land. Everything after it is a settled 2.
- Cells from `mid` to `hi` are unexamined.

```text
 [ 0 ... 0 | 1 ... 1 | ? ... ? | 2 ... 2 ]
            ^lo       ^mid     ^hi
   zeros      ones     unknown    twos
```

At the start `lo = mid = 0` and `hi = len(nums) - 1`: everything is unknown.

## Step by step

Take `[2, 0, 2, 1, 1, 0]`. Each round looks at `nums[mid]`.

```text
start        [2, 0, 2, 1, 1, 0]   lo=0 mid=0 hi=5

mid sees 2:  swap with hi, hi -= 1, mid stays
             [0, 0, 2, 1, 1, 2]   lo=0 mid=0 hi=4

mid sees 0:  swap with lo (itself), lo += 1, mid += 1
             [0, 0, 2, 1, 1, 2]   lo=1 mid=1 hi=4

mid sees 0:  lo += 1, mid += 1
             [0, 0, 2, 1, 1, 2]   lo=2 mid=2 hi=4

mid sees 2:  swap with hi, hi -= 1, mid stays
             [0, 0, 1, 1, 2, 2]   lo=2 mid=2 hi=3

mid sees 1:  mid += 1
             [0, 0, 1, 1, 2, 2]   lo=2 mid=3 hi=3

mid sees 1:  mid += 1
             [0, 0, 1, 1, 2, 2]   lo=2 mid=4 hi=3   mid > hi, stop
```

## Why it works

The four zones always partition the array, and every move extends exactly one settled zone by one cell:

- A 0 is swapped to `lo` and both `lo` and `mid` step on. The value that comes back to `mid` was in the ones zone (or was `mid` itself), so it is a known 1 and can be passed over.
- A 1 is already in the right zone, so `mid` just steps on.
- A 2 is swapped to `hi`, and `hi` steps back.

The unknown zone shrinks by one every round, so the loop ends when it is empty.

## Where it goes wrong

After swapping with `hi`, do not advance `mid`. The value that arrived from the back has never been looked at; it might be a 0 that still has to go left.

```text
[1, 2, 0]   lo=0 mid=1 hi=2
mid sees 2: swap with hi -> [1, 0, 2], hi=1
If mid advanced to 2 now, the 0 at index 1 would be skipped: wrong.
Correct: mid stays at 1, sees 0, swaps with lo -> [0, 1, 2].
```

Moving `mid` after a swap with `lo` is safe, though, because what lands at `mid` is a settled 1. Also loop while `mid <= hi`, not `mid < hi`, so the last unknown cell is examined.

## Cost

Time O(n): `mid` and `hi` together cross each cell once. Space O(1): sorted in place.
