## The idea

We want the three-number sum that lands nearest a target. Trying every triple is O(n³). As in 3Sum, sort first, fix one number, and use two pointers for the other two. The difference is that no sum has to be exact. Instead we keep a running best and nudge the pointers toward the target.

On a sorted array, a sum below the target can only be raised by moving `left` up, and a sum above it can only be lowered by moving `right` down. So each step moves toward the target without skipping any better candidate.

## Set-up

- `nums.sort()` makes the pointer moves meaningful.
- `best` is the sum nearest the target seen so far. It starts as the sum of the first three numbers, so it is always a real triple sum even if the target is far away.
- `i` fixes the first number; `left = i + 1`, `right = len(nums) - 1`.

```text
nums = [-1, 2, 1, -4]   target = 1     sorted -> [-4, -1, 1, 2]

 idx:   0   1   2   3
       -4  -1   1   2         best = -4 + -1 + 1 = -4
        ^   ^        ^
        i  left    right
```

## Step by step

```text
i=0 (-4), left=1, right=3:  -4 + -1 + 2 = -3
          |-3 - 1| = 4 beats |-4 - 1| = 5     best = -3
          -3 < 1, so left++

i=0 (-4), left=2, right=3:  -4 +  1 + 2 = -1
          |-1 - 1| = 2 beats 4               best = -1
          -1 < 1, so left++   (left meets right)

i=1 (-1), left=2, right=3:  -1 +  1 + 2 =  2
          |2 - 1| = 1 beats 2                best = 2
          2 > 1, so right--   (pointers meet)

i=2 stops: range(len(nums) - 2) ends at i=1.
return best = 2
```

If a sum equals the target, the function returns it at once, because nothing can be closer.

## Why it works

For a fixed `i`, the two-pointer sweep visits, for every `left`, the one `right` that straddles the target. Any pair it passes over would be further from the target than one it already examined. Running this for every `i` and keeping the smallest distance gives the global best.

## Where it goes wrong

- Starting `best` at `0` or at infinity can be wrong or break arithmetic. Using the first three numbers guarantees a valid candidate.
- Comparing distances needs `abs(...)` on both sides; comparing the sums directly would favour small sums over close ones.
- The target may be outside every reachable sum, as with a huge target. Then the sweep simply ends at the largest or smallest triple, which is correct.

## Cost

Time O(n²): the sort is O(n log n), and each of the n anchors makes an O(n) sweep. Space O(1) beyond the sort.
