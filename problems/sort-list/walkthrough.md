## The idea

Sorting a linked list rules out the usual array tricks. There is no random access, so quicksort's partitioning and heap sort's indexing are awkward. Merge sort fits well: splitting a list in the middle needs only a walk, and merging two sorted lists just relinks existing nodes with no extra storage.

So the plan is the textbook one. Cut the list in two, sort each half by the same method, then merge the two sorted halves. A list of zero or one node is already sorted, which ends the recursion.

## Set-up

- Base case: `head is None` or `head.next is None` returns `head` unchanged.
- `slow`, `fast` find the middle. `slow` moves one node per step, `fast` moves two. `fast` starts one node ahead, at `head.next`, so that `slow` ends on the LAST node of the first half.
- `second` is the head of the second half, taken as `slow.next`. Then `slow.next = None` cuts the list so the first half really stops.
- `merge` uses `dummy`, a placeholder head, and `tail`, the end of the merged list so far.

```text
head: 4 ──▶ 2 ──▶ 1 ──▶ 3 ──▶ None
      slow  fast
```

## Step by step

Sort `4 → 2 → 1 → 3`.

```text
Split:  fast hops 2 nodes while slow hops 1.
   slow=4 fast=2   fast.next is 1, so continue
   slow=2 fast=3   fast.next is None, stop
   second = slow.next = 1,  then cut slow.next = None

   4 ──▶ 2 ──▶ None          1 ──▶ 3 ──▶ None
```

Each half splits again into single nodes, which are sorted by definition, and merging builds back up:

```text
sortList(4 → 2)
   sortList(4) = 4      sortList(2) = 2
   merge(4, 2):  2 ──▶ 4

sortList(1 → 3)
   sortList(1) = 1      sortList(3) = 3
   merge(1, 3):  1 ──▶ 3
```

The final merge of `2 → 4` and `1 → 3`:

```text
a = 2 → 4     b = 1 → 3      dummy ──▶ None

take b (1 < 2):   dummy ──▶ 1             a = 2 → 4   b = 3
take a (2 <= 3):  dummy ──▶ 1 ──▶ 2       a = 4       b = 3
take b (3 < 4):   dummy ──▶ 1 ──▶ 2 ──▶ 3 a = 4       b = None
loop ends; attach the rest:  tail.next = a
                  dummy ──▶ 1 ──▶ 2 ──▶ 3 ──▶ 4
```

`merge` returns `dummy.next`, the head `1`.

## Why it works

If both halves come back sorted, merging them by always taking the smaller front node produces a sorted list. Each recursive call is on a strictly shorter list, so the recursion ends at the base case. Taking from `a` on ties (`<=`) keeps equal values in their original order.

## Where it goes wrong

- Forgetting `slow.next = None`. The first half would still run into the second, and the recursion would sort overlapping lists, never shrinking.
- Starting `fast` at `head` instead of `head.next`. With two nodes `[1, 2]`, `slow` would land on the second node, `second` would be `None`, and the first half would still have two nodes: infinite recursion.

```text
Two nodes 1 ──▶ 2, fast starts at head.next:
   fast.next is None, loop does not run, slow = 1
   halves:  1   and   2        (both smaller, good)
```

## Cost

Time O(n log n): the list halves about log n times, and each level does O(n) work in splitting and merging. Space O(log n) for the recursion stack; the merge itself allocates only one dummy node.
