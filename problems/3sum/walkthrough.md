## The idea

Finding triplets that sum to zero by brute force means three nested loops, O(n³), plus a lot of dedup work. Two observations cut it down.

First, sort the array. Then fix one number, `nums[i]`, and the question becomes: find two numbers to its right that add up to `-nums[i]`. On a sorted array that is a two-pointer sweep: O(n) rather than O(n²). Second, sorting puts equal values side by side, so skipping duplicates is just comparing a neighbour.

## Set-up

- `nums.sort()` lets us reason about "too small" and "too big".
- `i` is the anchor, the smallest value of the triplet.
- `left = i + 1` and `right = n - 1` close in on the rest.
- `result` collects triplets.

Invariant for the sweep: any pair that includes an index outside `[left, right]` has already been ruled out for this anchor.

```text
nums = [-1, 0, 1, 2, -1, -4]  sorted ->  [-4, -1, -1, 0, 1, 2]

 idx:   0   1   2   3   4   5
       -4  -1  -1   0   1   2
        ^   ^                ^
        i  left            right
```

## Step by step

```text
i=0 (-4): left=1, right=5   -4 + -1 + 2 = -3   too small, left++
          left=2            -4 + -1 + 2 = -3   too small, left++
          left=3            -4 +  0 + 2 = -2   too small, left++
          left=4            -4 +  1 + 2 = -1   too small, left++
          pointers meet, anchor done.

i=1 (-1): left=2, right=5   -1 + -1 + 2 =  0   hit! record [-1,-1,2]
          left=3, right=4   -1 +  0 + 1 =  0   hit! record [-1,0,1]
          pointers meet, anchor done.

i=2 (-1): same value as nums[1], skip (it would repeat the same triplets).

i=3 (0):  left=4, right=5    0 +  1 + 2 =  3   too big, right--
          pointers meet. Done.

result = [[-1, -1, 2], [-1, 0, 1]]
```

## Why it works

For a fixed anchor, if the sum is too small, the only way to raise it is to move `left` right, since `right` is already the largest remaining value. If it is too big, only moving `right` left can lower it. Either way the pointer being moved can never take part in a solution, so discarding it is safe, and the sweep covers every possible pair.

## Where it goes wrong

Duplicates are the trap. There are three places to skip them:

- the anchor: `nums[i] == nums[i - 1]` after the first index;
- `left` after a hit: step past equal values;
- `right` after a hit: step past equal values.

Without the anchor skip, the second `-1` above would find `[-1, 0, 1]` again.

```text
no anchor skip, i=2 (-1):  left=3, right=5   -1 + 0 + 2 = 1   too big
                           left=3, right=4   -1 + 0 + 1 = 0   [-1, 0, 1] again
```

The early `break` when `nums[i] > 0` is an optimisation: with the smallest value positive, every sum is positive.

## Cost

Time O(n²): the sort is O(n log n) and each of the n anchors does an O(n) sweep. Space O(1) beyond the output, ignoring the sort's own working space.
