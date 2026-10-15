## The idea

To find the kth largest we do not need the whole array sorted. We only need to remember the `k` largest values and know the smallest of those, because that is exactly the kth largest overall. A min-heap of size `k` does this: the root is always the smallest member of the heap.

When a new number arrives, it only matters if it beats the current root. If so, it replaces the root. Sorting everything costs O(n log n); this costs O(n log k).

## Set-up

- `heap` is a min-heap holding the `k` largest numbers seen so far (fewer at the start).
- `heap[0]`, the root, is the smallest of those, so it is the current candidate for the answer.

Invariant: after each number, `heap` contains the largest `min(k, count seen)` values.

```text
nums = [3, 2, 1, 5, 6, 4]    k = 2
heap = []
```

## Step by step

While the heap has fewer than `k` items we push. After that a number must exceed `heap[0]` to get in, and `heapq.heapreplace` pops the root and pushes the new value in a single step.

```text
num=3   heap size 0 < 2 -> push                   heap = [3]
num=2   heap size 1 < 2 -> push                   heap = [2, 3]
num=1   1 > heap[0]=2? no, skip                   heap = [2, 3]
num=5   5 > 2 -> replace root 2 with 5            heap = [3, 5]
num=6   6 > 3 -> replace root 3 with 6            heap = [5, 6]
num=4   4 > 5? no, skip                           heap = [5, 6]

return heap[0] = 5
```

```text
final heap:    5          the two largest values are 6 and 5;
              /           the smaller of them is the 2nd largest
             6
```

## Why it works

A number that is smaller than the `k`th best seen so far can never become the kth largest later, because there are already `k` larger ones. Numbers that beat the root push out the old kth largest, which is then no longer among the top `k`. At the end the heap is exactly the `k` largest values, and the smallest of them is the kth largest.

## Where it goes wrong

- A max-heap of everything gives the right answer but needs O(n) space and O(n log n) time. The min-heap of size `k` is the trick.
- Using `>=` instead of `>` when comparing to the root works but does pointless replacements for duplicates. Duplicates count separately: in `[3,2,3,1,2,4,5,5,6]` with `k=4`, both 5s occupy slots.
- Returning `heap[-1]` is wrong; a heap list is not sorted, only the root is guaranteed.

## Other approaches

Quickselect partitions around a pivot and recurses on one side only, giving average O(n) time and O(1) extra space, but O(n^2) on bad pivots and it reorders the array.

## Cost

Time O(n log k): every number costs at most one O(log k) heap operation. Space O(k).
