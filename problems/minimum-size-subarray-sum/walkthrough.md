## The idea

We want the shortest contiguous run of numbers whose sum reaches `target`. Checking every start and end is O(n^2). Because every number is positive, a window gets bigger sum when it grows and smaller sum when it shrinks. That one fact means we never need to move a pointer backwards: a sliding window finds the answer in one pass.

Grow on the right until the window is big enough. Then shrink from the left as far as possible while it stays big enough, noting the shortest length on the way.

## Set-up

- `left` is the start of the window; `right` (from `enumerate`) is its end. The window is `nums[left..right]`.
- `total` is the sum of the window. Invariant: after the inner loop, `total < target` (or the window is empty).
- `best` starts at `len(nums) + 1`, a length no real window can have. It is both the running minimum and the "not found" marker.

```text
target = 7
nums   = [2, 3, 1, 2, 4, 3]
          ^
        left, right

total = 0, best = 7
```

## Step by step

For each `right`: add `nums[right]`, then while `total >= target` record `right - left + 1`, subtract `nums[left]`, move `left` forward.

```text
right=0  add 2   total=2                       too small
right=1  add 3   total=5                       too small
right=2  add 1   total=6                       too small
right=3  add 2   total=8  >= 7
           window [2,3,1,2] len 4 -> best=4
           drop 2 -> total=6, left=1
right=4  add 4   total=10 >= 7
           window [3,1,2,4] len 4 -> best=4
           drop 3 -> total=7, left=2
           7 >= 7: window [1,2,4] len 3 -> best=3
           drop 1 -> total=6, left=3
right=5  add 3   total=9  >= 7
           window [2,4,3] len 3 -> best=3
           drop 2 -> total=7, left=4
           7 >= 7: window [4,3] len 2 -> best=2
           drop 4 -> total=3, left=5
```

```text
final window state:   [2, 3, 1, 2, 4, 3]
                                      ^ left=5, right=5
best = 2  (window [4, 3])
```

## Why it works

When the window `[left, right]` first reaches `target`, shrinking from the left finds the shortest window ending at `right`. Dropping `nums[left]` further would fall below `target`. Any later window ending at a bigger `right` and starting before `left` would contain a window we already tried and is longer, so `left` never needs to go back. Positivity is what guarantees this.

## Where it goes wrong

- Using `if` instead of `while` for the shrink step. After one drop the window can still be big enough (as at `right=4` above, where `7 >= 7` still holds), and you would miss the shorter answer.
- Returning `best` unchanged when nothing qualified. It would be `len(nums) + 1`, so the final line maps that to `0`.
- With negative numbers the monotonic argument breaks. This solution relies on positive input.

```text
if instead of while, right=4:
  window [3,1,2,4] total 10 -> drop one -> [1,2,4] total 7, still enough,
  but the loop moves on: the length-3 window is never recorded, the window
  stays too wide, and the function returns 4 instead of 2.
```

## Cost

Time O(n): `left` and `right` each move forward at most n times. Space O(1): a few integers.
