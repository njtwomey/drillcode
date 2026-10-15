## The idea

The median is the middle of the sorted data. To read it you do not need the whole list sorted, only the boundary: the largest of the smaller half and the smallest of the larger half. Keep the numbers split into two halves and the median sits right at the seam.

A heap hands you its extreme in O(1) and takes inserts in O(log n). The lower half wants its LARGEST on top, and the upper half wants its SMALLEST on top. So the lower half is a max-heap and the upper half is a min-heap. Re-sorting after every insert would cost O(n log n) per call, or O(n) with insertion into a sorted list. Two heaps keep it to O(log n).

## Set-up

- `low` holds the smaller half. Python's `heapq` is a min-heap only, so values are stored negated: the smallest stored value is the largest real one.
- `high` holds the larger half, as a plain min-heap.

Two invariants hold after every `addNum`:

- Every value in `low` is `<=` every value in `high`.
- `len(low)` equals `len(high)`, or is exactly one bigger. So with an odd count the median is `low`'s top, and with an even count it is the average of the two tops.

```text
low (max-heap, shown as real values)     high (min-heap)

   top of low  ──▶ 10 ┐                       ┌ 50 ◀── top of high
                       1 ┘                    └ 100

   sorted view:   1  10 │ 50  100            median = (10 + 50) / 2
                        ^ the seam
```

## Step by step

Each add does three things: push `num` into `low`, pop `low`'s top into `high`, and if `high` now has more elements, move its top back to `low`. The detour through `low` guarantees the biggest of the lower half crosses over, so ordering holds without comparing against the tops by hand. Adding 10, 1, 100, 50, 2 (heaps shown as real values):

```text
add 10    low {10}        high {}          median 10
          push to low, move 10 to high, high is bigger, move it back

add 1     low {1}         high {10}        median (1 + 10) / 2 = 5.5
          1 goes into low, the max (10) crosses to high

add 100   low {10, 1}     high {100}       median 10
          100 crosses to high, high is now 2 vs 1,
          so its min (10) moves back to low

add 50    low {10, 1}     high {50, 100}   median (10 + 50) / 2 = 30
          50 crosses to high, sizes are 2 and 2, nothing moves back

add 2     low {10, 2, 1}  high {50, 100}   median 10
          2 enters low, 10 crosses to high, then high is bigger, 10 returns
```

## Why it works

Pushing into `low` and then taking `low`'s maximum guarantees the value moved to `high` is at least as large as everything left in `low`, and it is no larger than `high`'s existing members only if it should be. When the new value is big, it is itself the max and passes straight through. When it is small, the old max of `low` crosses instead, so ordering between halves is preserved. The final size check keeps `low` the same size or one bigger, so the median is always at the tops.

## Where it goes wrong

- Forgetting to negate. Without `-num` in `low`, the top would be the smallest of the lower half and the median would be wrong.
- Pushing straight into whichever heap looks right based on a comparison with a top, and forgetting the empty-heap case.
- Letting `high` grow bigger than `low`. With three numbers the median would be read from the wrong place.
- Returning an integer. `findMedian` returns a float, so the odd case does `float(-self.low[0])`.

## Cost

`addNum` is O(log n): a constant number of heap operations. `findMedian` is O(1): read one or two tops. Space O(n) to store every number.
