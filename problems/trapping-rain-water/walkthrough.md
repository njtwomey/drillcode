## The idea

Water sitting above a bar is bounded by the shorter of the two tallest walls on either side: `min(tallest to the left, tallest to the right) - height`. Computing both maxima for every bar needs two extra arrays.

Two pointers avoid that. Keep one pointer at each end and the running maximum seen from each end. At any moment, whichever end has the shorter bar is the one whose water is already decided, because the taller bar on the other side guarantees the "right wall" is at least as tall as the left one.

## Set-up

- `left`, `right` are the two pointers, moving inward.
- `left_max`, `right_max` are the tallest bars seen so far from each end.
- `total` is the water so far.

The invariant: every bar outside `[left, right]` has already been counted correctly.

```text
height = [4, 2, 0, 3, 2, 5]

 index   0  1  2  3  4  5
 height  4  2  0  3  2  5
         ^                ^
        left            right
left_max = 0   right_max = 0   total = 0
```

## Step by step

Compare `height[left]` and `height[right]`. The smaller side moves: update its max, add `max - height`, step inward.

```text
left=0 (4) < right=5 (5)   left_max=4   add 0   total 0    left -> 1
left=1 (2) < 5             left_max=4   add 2   total 2    left -> 2
left=2 (0) < 5             left_max=4   add 4   total 6    left -> 3
left=3 (3) < 5             left_max=4   add 1   total 7    left -> 4
left=4 (2) < 5             left_max=4   add 2   total 9    left -> 5
left == right, stop
```

```text
 level 5   .  .  .  .  .  #
 level 4   #  ~  ~  ~  ~  #
 level 3   #  ~  ~  #  ~  #
 level 2   #  #  ~  #  #  #
 level 1   #  #  ~  #  #  #
 height    4  2  0  3  2  5      # bar, ~ water: 2 + 4 + 1 + 2 = 9
```

Here the right side never moves because bar 5 is the tallest: every left bar is bounded by `left_max = 4`, as the wall on the right is always at least 5.

## Why it works

Suppose `height[left] < height[right]`. Some bar at or beyond `right` is at least `height[right]`, so the right-hand wall for `left` is at least as tall as every bar the left pointer has accepted so far (each was accepted under the same test, against a right bar that is still in place or taller). The water above `left` is then limited by the left wall alone, which is `left_max`, so `left_max - height[left]` is exact. The `else` branch is the mirror image. Each step finalises one bar and shrinks the unknown middle by one.

## Where it goes wrong

- Adding water before updating `left_max` (or `right_max`) gives a negative amount when a new tallest bar arrives. The code updates first, so that bar contributes 0.
- Moving the wrong pointer, for example always moving `left`, breaks the guarantee that the other wall is tall enough.
- Fewer than three bars gives 0, since the loop finds nothing to hold.

## Cost

Time O(n): each step moves one pointer inward. Space O(1).

## Other approaches

Build `prefix_max` and `suffix_max` arrays and sum `min(prefix, suffix) - height`. It is the same O(n) time but uses O(n) space.
