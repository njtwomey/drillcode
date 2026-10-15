## The idea

We want the `k` points nearest the origin. Sorting every point by distance works but does more than needed: O(n log n) to order points we will throw away. Instead keep a small bucket of the best `k` seen so far. When a new point arrives, it either belongs in the bucket or not; if the bucket overflows, evict the worst member.

"The worst member" is the largest distance, and a max-heap hands that over in O(log k). Python's `heapq` is a min-heap, so we store the negated distance.

## Set-up

- `heap` holds tuples `(-squared distance, index)`. The root is the smallest tuple, i.e. the most negative, i.e. the farthest point.
- Squared distance `x*x + y*y` orders points the same as true distance, so no square root.
- Storing the index (not the point) keeps the tuples comparable and lets us look the point up at the end.

Invariant: after each point, `heap` holds the closest `min(k, points seen)` points.

```text
points = [[3,3], [5,-1], [-2,4]]     k = 2

squared distances:  index 0: 18    index 1: 26    index 2: 20
heap = []
```

## Step by step

```text
push (-18, 0)             heap = [(-18,0)]               size 1

push (-26, 1)             heap = [(-26,1), (-18,0)]      size 2
                          root is the farthest so far (26)

push (-20, 2)             size 3 > k, so pop the root:
                          removed (-26, 1)  -> point [5,-1], distance 26
                          heap = [(-20,2), (-18,0)]
```

```text
final heap (a binary heap stored as a list):

        (-20, 2)
        /
   (-18, 0)           answer: points[2], points[0] = [-2,4], [3,3]
```

The result comes out in heap order, not sorted by distance. The problem accepts any order.

## Why it works

Each time the heap overflows, the point removed is the farthest among the `k + 1` held, so it can never be among the final `k` closest: there are already `k` closer points. The ones that survive to the end are therefore the `k` closest overall.

## Where it goes wrong

- Using a min-heap with positive distances keeps the `k` farthest points instead of the closest. The negation is what makes the root the worst one.
- Pushing the bare point list into the heap breaks on ties, because Python would compare lists. The index breaks ties without comparing points.
- Popping when `len(heap) >= k` rather than `> k` leaves you with `k - 1` points.

## Other approaches

Quickselect partitions the points around a pivot distance like quicksort but only recurses into the side containing position `k`. It averages O(n) time but is O(n^2) in the worst case and rearranges the input. The heap is steadier and works on a stream.

## Cost

Time O(n log k): each of `n` points does one push and at most one pop on a heap of size at most `k + 1`. Space O(k) for the heap.
