## The idea

Merging both arrays and picking the middle is O(m + n). To do better, notice that the median is defined by a cut. Split the combined sorted data into a left half and a right half of (almost) equal size: the median is at the seam. The cut is correct when everything on the left is `<=` everything on the right.

You do not have to merge to find such a cut. The left half is made of a prefix of the first array and a prefix of the second. Choose how many to take from the first, `i`, and the second is forced: `j = half - i`. Because both arrays are sorted, the cut is correct as soon as the elements next to it satisfy two comparisons. And when it is wrong, the failing comparison tells you whether `i` was too big or too small, so binary search on `i` works.

## Set-up

- `a` is the shorter array and `b` the longer. Searching the shorter one keeps the range small and means `j` never leaves `b`'s bounds.
- `half = (m + n + 1) // 2` is the size of the left half. With an odd total it has one extra element, so the median is the biggest element on the left.
- `lo, hi = 0, m` is the search range for `i`, the number of elements of `a` on the left.
- Four values next to the cut: `a_left`, `a_right`, `b_left`, `b_right`. When a side is empty, `-inf` or `inf` stands in, so no special cases are needed.

```text
a = [1, 2, 3]      b = [10, 20, 30, 40]      m=3  n=4  half=4

a:  1  2  3            a cut at i leaves i elements on the left
b:  10 20 30 40        the b cut is j = half - i, so the left side
                       always has i + j = 4 elements
```

## Step by step

A valid cut needs `a_left <= b_right` and `b_left <= a_right`. If `a_left > b_right`, `a` gave too many, so `hi = i - 1`. If `b_left > a_right`, `a` gave too few, so `lo = i + 1`.

```text
Round 1  lo=0 hi=3  i=1  j=3
   a:  1 | 2 3              a_left=1    a_right=2
   b:  10 20 30 | 40        b_left=30   b_right=40
   b_left 30 > a_right 2    a gave too few       lo = 2

Round 2  lo=2 hi=3  i=2  j=2
   a:  1 2 | 3              a_left=2    a_right=3
   b:  10 20 | 30 40        b_left=20   b_right=30
   b_left 20 > a_right 3    still too few        lo = 3

Round 3  lo=3 hi=3  i=3  j=1
   a:  1 2 3 |              a_left=3    a_right=inf
   b:  10 | 20 30 40        b_left=10   b_right=20
   3 <= 20 and 10 <= inf    valid cut
```

The total is 7, which is odd, so the answer is `max(a_left, b_left)` = `max(3, 10)` = 10.0. With an even total it would be the average of `max(a_left, b_left)` and `min(a_right, b_right)`. For `[1, 3, 5, 7]` and `[2, 4, 6, 8]` the first cut tried is already valid: left side `1 3 | 2 4`, giving `(4 + 5) / 2 = 4.5`.

## Why it works

If both arrays are sorted and `a_left <= b_right` and `b_left <= a_right`, then every element on the left is `<=` every element on the right. Within `a` and within `b` that follows from sorting, and the two cross comparisons cover the rest. The left side has exactly `half` elements, so the median sits at the seam. Moving `i` right moves `j` left, so `a_left` and `b_right` only get bigger or smaller together. That monotonic behaviour is what lets binary search home in on the cut.

## Where it goes wrong

- Searching the longer array. Then `j = half - i` can go negative or past the end of `b`.
- Using `half = (m + n) // 2`. With an odd total the middle element would end up on the right and the odd branch would return the wrong value.
- Special-casing empty sides with extra `if`s. `-inf` and `inf` make the comparisons pass naturally. An empty `a` gives `i = 0`, `a_left = -inf`, and the median comes from `b` alone.
- Returning an int. The result is a float, so the odd case wraps it in `float(...)`.

## Cost

Time O(log min(m, n)): the binary search runs on the shorter array only. Space O(1): a handful of variables.
