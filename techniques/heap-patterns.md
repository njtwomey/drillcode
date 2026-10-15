---
title: Heap patterns
area: Heaps
topics: [Heap]
problems:
  - kth-largest-element-in-an-array
  - k-closest-points-to-origin
  - top-k-frequent-elements
  - merge-k-sorted-lists
  - find-median-from-data-stream
  - meeting-rooms-ii
  - last-stone-weight
  - top-k-frequent-words
  - find-k-pairs-with-smallest-sums
  - reorganize-string
  - task-scheduler
  - sliding-window-median
  - kth-largest-element-in-a-stream
  - design-twitter
  - minimum-interval-to-include-each-query
  - kth-smallest-element-in-a-sorted-matrix
related: [interval-patterns, dummy-head, design-structures, sliding-window, greedy-one-pass-invariants]
---
## Reach for it when

- The statement says "k-th largest", "top k", "k closest" or "k most frequent".
- k sorted sources must be merged into one ordered stream.
- The two largest (or most frequent) items must be taken repeatedly, with the remainder put back.
- A schedule or arrangement must separate equal items by a gap.
- A running median or other order statistic is needed while data keeps arriving.
- The next thing to handle is always the earliest-ending (or smallest, or nearest) of many pending things, as in room allocation.
- Queries or events can be answered offline in sorted order while a heap holds the candidates that are still valid.
- Sorting everything would work but costs O(n log n) when O(n log k) is wanted.

## Setup

- `heap = []`: a plain list managed by `heapq`. It is a min-heap; `heap[0]` is the smallest entry. Invariant: `heap[0]` is the minimum at all times.
- Max-heap: push `-value` and negate again when reading. Invariant: everything stored is negated, and every read negates back.
- Entries that carry data: use tuples `(key, i, item)`. Tuples compare element by element, so a unique `i` before any object that cannot be compared (a `ListNode`) means the objects are never reached.
- Top k: bound the heap to size `k`. Invariant after each step: the heap holds the k best seen so far, and its root is the worst of them, which is the one to evict.
- Two heaps: `low` is a max-heap (negated) for the smaller half and `high` is a min-heap for the larger half. Invariant: every value in `low` is at most every value in `high`, and the sizes differ by at most one.
- Counts as heap keys: push `(-count, item)` so the most frequent item pops first and ties fall back to the item. Invariant: each entry holds the count still unused.
- `best` or a running maximum of `len(heap)` if the answer is a peak count.

## Template

```python
import heapq


def top_k_largest(items, k):
    heap = []
    for i, item in enumerate(items):
        heapq.heappush(heap, (item, i))
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted((item for item, _ in heap), reverse=True)
```

`top_k_largest([3, 1, 5, 2, 8, 5], 3)` returns `[8, 5, 5]`. A min-heap of size k keeps the k largest: the smallest of them sits at the root and is the first to go. For the k smallest, negate the key.

## What it removes

- A full sort. A heap of size k costs O(n log k) time and O(k) space, and the stream version never needs all the data at once.
- Re-scanning for the minimum. Each push and pop is O(log size), against O(size) for a linear scan.
- In k-way merge, comparing k heads at every step. The heap holds only the current head of each list, so it never exceeds k entries.
- In the median problem, keeping everything sorted. Only the two middle values matter, and the two tops give them directly.

## Pitfalls

- Missing tiebreaker. `heappush(heap, (node.val, node))` raises `TypeError` the first time two values are equal. Put a unique index in the middle.
- Forgetting to negate on the way out. A max-heap built by negation returns `-8` instead of `8`, or the median comes out with the wrong sign.
- Using a min-heap of size k for "k smallest". It keeps the k largest. For the k smallest, evict the largest, which means negating the key.
- Pushing to the wrong heap. If a new value goes straight into `high` without passing through `low`, a value smaller than `low`'s top breaks the ordering and the median is wrong.
- Forgetting the rebalance step. Sizes drift apart and `low[0]` is no longer a middle value.
- Comparing the heap size with `k` before pushing in some places and after in others, giving a heap of size k + 1 or k - 1. Pick one form.
- Pushing a spent item back. In `reorganize-string`, a letter whose count reached zero must not return to the heap, or the loop emits it again.
- Taking only one item per round where two are needed, or leaving a lone last letter unhandled. `reorganize-string` ends with at most one entry in the heap and must append it.
- Using the formula `(most - 1) * (n + 1) + tied` without the floor. `task-scheduler` with many distinct tasks and a small `n` gives a number below `len(tasks)`; the answer is the larger of the two.
- In `kth-largest-element-in-a-stream`, replacing the root before the heap holds k values. `add` must `heappush` until `len(heap) == k`; only then does `heap[0]` mean the kth largest. The constructor feeds `nums` through `add`, so a short or empty initial list is handled by the same code.
- In `design-twitter`, pushing every tweet of every followee. Only the newest per user is needed; push the previous one (`idx - 1`) after popping a user's tweet, and stop at 10.
- In `minimum-interval-to-include-each-query`, answering queries in input order. The sweep needs them sorted, so keep each query's original index and write `result[idx]`. Also check `heap[0][1] < q` only at the top: an expired interval buried lower is removed when it surfaces, which is enough.
- In `kth-smallest-element-in-a-sorted-matrix`, seeding all n rows when k is small, or pushing `c + 1` without the `c + 1 < n` check. Seed `min(n, k)` rows and stop a row at its last column.
- Treating the heap as sorted. Only `heap[0]` is guaranteed; iterating the list does not give sorted order.

## Variants

- Top k with a bounded heap, `kth-largest-element-in-an-array`: push until the heap holds k, after that replace the root only when the new value beats it, using `heapreplace` for a single O(log k) step. The answer is `heap[0]`. Quickselect (partition, then recurse into one side) is the O(n) average alternative; the catalogue solution uses the heap.
- Heap of tuples with a computed key, `k-closest-points-to-origin`: key is the negated squared distance, with the point's index as the second element. Squared distance orders the same as distance, so there is no square root. The index points back into the input, so the points themselves are never compared.
- Bounded counts, `top-k-frequent-elements`: no heap is needed. Frequencies are at most `len(nums)`, so bucket by frequency and walk from the top. A heap of size k over `(count, value)` is the alternative; the bucket form is O(n).
- k-way merge, `merge-k-sorted-lists`: seed the heap with `(node.val, i, node)` for each non-empty list, pop the smallest, attach it, and push its successor. This is the case where the tiebreaker matters.
- Two heaps, `find-median-from-data-stream`: to add a value, push it into `low`, move `low`'s top to `high`, then move one back if `high` is larger. The median is `low`'s top for an odd count, otherwise the average of both tops. This solution keeps the extra element in `low`.
- Earliest finishing, `meeting-rooms-ii`: a min-heap of end times of meetings holding a room. If the smallest end is at or before the next start, reuse that room with `heapreplace`; otherwise push. The largest heap size seen is the answer. See `interval-patterns`.
- Repeated max with put-back, `last-stone-weight`: store `-stone`, pop two, and push `-(first - second)` only if they differ. The answer is `-heap[0]`, or 0 for an empty heap.
- Top k with a composite key, `top-k-frequent-words`: no explicit heap code. `heapq.nsmallest(k, count, key=lambda word: (-count[word], word))` orders by higher count, then alphabetically. It is O(n log k).
- Lazy k-way merge of an implicit grid, `find-k-pairs-with-smallest-sums`: each `i` is a sorted row of sums `nums1[i] + nums2[j]`. Seed `(sum, i, 0)` for the first `min(k, len(nums1))` rows, pop, then push `(i, j + 1)`. Rows past k can never reach the top k.
- Pair the two largest, `reorganize-string`: return `""` when the top count exceeds `(len(s) + 1) // 2`. Otherwise pop two `(-count, letter)` entries each round, append both letters, and push back those with count left.
- A formula in place of a heap, `task-scheduler`: the most frequent task fixes `(most - 1)` frames of length `n + 1`, plus a last row of `tied` tasks. The answer is `max(len(tasks), frames)`. A heap simulation gives the same answer in more code.
- Bounded min-heap over a stream, `kth-largest-element-in-a-stream`: `heap` holds the k largest values seen, so `heap[0]` is the kth largest. `add` pushes while `len(heap) < k`, then uses `heapreplace` only when `val > heap[0]`; anything else cannot be in the top k. The constructor calls `add` for each of `nums`.
- Merge of time-ordered lists, `design-twitter`: each user's `tweets[user]` is already sorted by time, so `getNewsFeed` is a k-way merge. The heap holds `(-time, tweetId, user, idx)` for each followee's newest tweet. After a pop, push the same user's tweet at `idx - 1`. Stop at 10 results. See `design-structures`.
- Offline sweep with lazy deletion, `minimum-interval-to-include-each-query`: sort `intervals` by start and iterate `sorted((q, idx) for idx, q in enumerate(queries))`. For each `q`, push `(right - left + 1, right)` for every interval with `left <= q`, then pop while `heap[0][1] < q`. The root is the smallest interval containing `q`, and `-1` stays if the heap is empty. Queries only grow, so an expired interval never becomes valid again. See `interval-patterns`.
- Heap of row heads, `kth-smallest-element-in-a-sorted-matrix`: seed `(matrix[r][0], r, 0)` for `r in range(min(n, k))`, heapify, pop `k - 1` times pushing `(matrix[r][c + 1], r, c + 1)` when `c + 1 < n`, and return `heap[0][0]`. Same shape as `find-k-pairs-with-smallest-sums`. The other approach is binary search on the value with a staircase count; see `binary-search-on-answer`.
- Order statistic of a window, `sliding-window-median`: the catalogue solution keeps `window` as a sorted list, removing the outgoing value with `bisect_left` and adding the new one with `insort`. It is O(n * k) because of the shifting, but simple. Two heaps with lazy deletion are the O(n log k) alternative. See `sliding-window`.

## Worked example

Problem: `kth-largest-element-in-an-array`

A min-heap bounded to k entries over the stream of numbers.

```python
class Solution:

    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            elif num > heap[0]:
                heapq.heapreplace(heap, num)
        return heap[0]
```

`heap` is the bounded min-heap from Setup. Its size is checked before pushing, so it never exceeds k. The root `heap[0]` is the smallest of the k largest values seen, which is the k-th largest overall, so it is both the eviction candidate during the loop and the answer after it. `heapreplace` pops the root and pushes `num` in one step. No tiebreaker is needed because the entries are plain integers.
