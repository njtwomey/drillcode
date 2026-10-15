## The idea

Sorting the whole stream after every new value would work, but it is slow and wasteful: you only ever need the kth largest. The values below that rank can never matter again.

So keep only the `k` largest values seen, in a min-heap. The root of a min-heap is the smallest value it holds. Among the `k` largest, the smallest is exactly the kth largest. The answer is always `heap[0]`.

## Set-up

- `self.k` is the target rank.
- `self.heap` is a min-heap that never holds more than `k` values. It contains the `k` largest numbers seen so far, or all of them if fewer than `k` have arrived.
- The constructor just calls `add` for each starting number, so the initial list follows the same rules as later values.

```text
k = 3

heap (min-heap, root is smallest):   {}    size 0
```

## Step by step

`add(val)` has three cases: heap not full yet, so push; full and `val` beats the root, so replace the root; otherwise ignore. Start with `nums = [4, 5, 8, 2]`.

```text
add 4  heap not full: push           heap {4}
add 5  heap not full: push           heap {4, 5}
add 8  heap not full: push           heap {4, 5, 8}   root 4
add 2  full, 2 > 4? no, ignore       heap {4, 5, 8}   root 4

Now the stream calls:
add 3  3 > 4? no, ignore             heap {4, 5, 8}   returns 4
add 5  5 > 4? yes, replace 4 by 5    heap {5, 5, 8}   returns 5
add 10 10 > 5? yes, replace 5        heap {5, 8, 10}  returns 5
add 9  9 > 5? yes, replace 5         heap {8, 9, 10}  returns 8
add 4  4 > 8? no, ignore             heap {8, 9, 10}  returns 8
```

Each returned value is the current root.

## Why it works

The heap always holds the `k` largest values so far. A new value either belongs among them, in which case it pushes the old smallest of the group out, or it is no larger than the smallest member and has at least `k` values at or above it, so it is not in the top `k`. Either way the invariant holds after the call, and the root is the smallest of the top `k`.

`heapreplace` pops the root and pushes the new value in one operation, which is cheaper than a separate pop and push.

## Where it goes wrong

- Using `>=` instead of `>`. Duplicates count separately, so an equal value changes nothing about the kth largest; replacing the root with an equal number is harmless but pointless.
- Using a max-heap. Then the root is the largest, and you cannot get the kth largest without removing `k - 1` values.
- A starting list shorter than `k`. The heap simply stays under `k` items until enough have arrived, and the problem promises `add` is only queried when an answer exists.

## Cost

Time O(log k) per `add`, since heap operations work on a heap of at most `k` items. Constructing from `nums` costs O(m log k) for `m` starting values. Space O(k).
