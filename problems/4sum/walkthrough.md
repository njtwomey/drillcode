## The idea

4Sum is 3Sum with one more loop. Sort the array, fix the first two numbers with nested loops (`i` and `j`), and finish with the two-pointer sweep from 3Sum on whatever is to the right. Brute force would be four nested loops, O(n⁴); this is O(n³).

Sorting does double duty. It makes the pointer moves valid (too small, move `left`; too big, move `right`), and it puts equal values next to each other so repeats can be skipped cheaply.

## Set-up

- `nums.sort()`.
- `i` is the first value and `j` is the second, with `j > i`.
- `left = j + 1` and `right = n - 1` close in on the remaining two.
- `result` collects quadruplets.

Invariant for the sweep: for the current `i`, `j`, any pair using an index outside `[left, right]` has already been ruled out.

```text
nums = [1, 0, -1, 0, -2, 2]   target = 0
sorted ->

 idx:   0   1   2   3   4   5
       -2  -1   0   0   1   2
        ^   ^   ^           ^
        i   j  left       right
```

## Step by step

```text
i=0 (-2), j=1 (-1):
  left=2, right=5   -2 + -1 + 0 + 2 = -1   too small, left++
  left=3, right=5   -2 + -1 + 0 + 2 = -1   too small, left++
  left=4, right=5   -2 + -1 + 1 + 2 =  0   hit! record [-2,-1,1,2]
i=0 (-2), j=2 (0):
  left=3, right=5   -2 +  0 + 0 + 2 =  0   hit! record [-2,0,0,2]
i=1 (-1), j=2 (0):
  left=3, right=5   -1 +  0 + 0 + 2 =  1   too big, right--
  left=3, right=4   -1 +  0 + 0 + 1 =  0   hit! record [-1,0,0,1]
i=2 (0),  j=3 (0):
  left=4, right=5    0 +  0 + 1 + 2 =  3   too big, right--, then meet.

result = [[-2,-1,1,2], [-2,0,0,2], [-1,0,0,1]]
```

After a hit, both pointers move inward and then skip over any equal values, so the same quadruplet is not recorded twice.

## Why it works

Fixing `i` and `j` reduces the rest to a sorted two-sum, and the sweep from both ends is complete for that: if the sum is too small, nothing paired with the current `left` and a smaller `right` can reach the target, so `left` is discarded; the mirror argument holds for `right`.

## Where it goes wrong

Duplicates need three guards, one per level, otherwise the same quadruplet appears several times:

- `i`: skip if `nums[i] == nums[i - 1]`.
- `j`: skip if `j > i + 1 and nums[j] == nums[j - 1]`.
- `left` and `right`: skip equal values after recording.

The `j > i + 1` condition is easy to get wrong. If you wrote `j > 0`, you would skip a legitimate second value that equals `nums[i]`. In the trace above, `i=2` and `j=3` are both 0, and that pair must still be tried.

```text
i=2 (0), j=3 (0): nums[j-1] == nums[j], but j == i+1, so NOT skipped.
```

## Cost

Time O(n³): two nested loops, each running an O(n) sweep. Space O(1) beyond the output and the sort.
