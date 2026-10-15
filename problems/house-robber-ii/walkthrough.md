## The idea

The street is now a circle, so the first and last houses are neighbours and cannot both be robbed. That sounds new, but it reduces to the straight-street problem. In any valid plan, either the last house is not robbed or the first one is not. So solve two straight streets and take the better:

- houses `0 .. n-2` (last house dropped),
- houses `1 .. n-1` (first house dropped).

Every legal plan fits inside at least one of those two slices, and each slice has no wrap-around conflict.

## Set-up

- `rob_line(houses)` is the plain House Robber recurrence. It keeps `prev` (best up to two houses back) and `curr` (best up to the previous house), both starting at 0.
- `nums[:-1]` and `nums[1:]` are the two slices.
- A single house is handled first: both slices would be empty and give 0, but the real answer is `nums[0]`.

```text
nums = [2, 3, 2]

slice A = nums[:-1] = [2, 3]       (drop the last house)
slice B = nums[1:]  = [3, 2]       (drop the first house)
```

## Step by step

Running `rob_line` on `[200, 3, 140, 20, 10]`, a case where the first and last houses both look tempting:

```text
Slice A = [200, 3, 140, 20]
 num   prev  curr
 200    0    200
   3  200    200
 140  200    340
  20  340    340      -> 340

Slice B = [3, 140, 20, 10]
 num   prev  curr
   3    0      3
 140    3    140
  20  140    140
  10  140    150      -> 150

answer = max(340, 150) = 340
```

The 200 and 140 are far apart in the line, so slice A takes both. Slice B cannot use the 200 at all, so it does worse.

## Why it works

If a plan uses the last house, it cannot use the first, so it lives in slice B. If it does not use the last house, it lives in slice A. Neither slice contains a wrap-around pair, so the linear recurrence is exact on each.

## Where it goes wrong

- With `n == 1` both slices are empty, so without the early return the answer would be 0.
- With `n == 2`, the slices are single houses, which correctly yields the larger of the two.
- Dropping a house from the slice is not the same as forbidding it: the other slice may still use it.

## Cost

Time O(n): two linear passes (slicing copies the list, also O(n)). Space O(n) for the slice copies; the DP itself uses O(1). Index bounds instead of slices would make it O(1) extra.
