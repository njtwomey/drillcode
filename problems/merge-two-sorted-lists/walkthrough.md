## The idea

Both lists are already sorted, so the smallest unused value overall is always one of the two front nodes. Compare the fronts, take the smaller, and repeat. This is the merge step of merge sort, and it needs no extra storage because we relink existing nodes instead of copying them.

The one awkward part is the very first node: which list does the result start with? A throwaway placeholder node removes that question.

## Set-up

- `dummy` is a fake node that sits before the real result. Its `next` will be the merged head.
- `tail` is the last node of the merged list so far. It starts as `dummy` itself, so the first real node attaches to `dummy.next` with the same code as every other node.
- `list1` and `list2` double as cursors at the first unused node of each list.

Invariant: everything from `dummy.next` to `tail` is sorted, and every value in it is no larger than anything still in `list1` or `list2`.

```text
dummy/tail
   │
  [ ]

list1: 1 ──▶ 2 ──▶ 4
list2: 1 ──▶ 3 ──▶ 4
```

## Step by step

With `list1 = 1,2,4` and `list2 = 1,3,4`. Each round attaches one node to `tail` and moves that list's cursor.

```text
Round 1  1 <= 1, take list1's 1.      merged: [ ] ─▶ 1a
         list1 at 2, list2 at 1b
Round 2  2 <= 1 is False, take 1b.    merged: [ ] ─▶ 1a ─▶ 1b
         list1 at 2, list2 at 3
Round 3  2 <= 3, take 2.              merged: [ ] ─▶ 1a ─▶ 1b ─▶ 2
         list1 at 4, list2 at 3
Round 4  4 <= 3 is False, take 3.     merged: [ ] ─▶ 1a ─▶ 1b ─▶ 2 ─▶ 3
         list1 at 4, list2 at 4b
Round 5  4 <= 4, take list1's 4.      merged: [ ] ─▶ 1a ─▶ 1b ─▶ 2 ─▶ 3 ─▶ 4a
         list1 is None: loop ends
```

Now `tail.next = list1 or list2` hooks the rest of `list2` (the lone `4b`) onto the end in one step:

```text
[ ] ─▶ 1 ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 4a ─▶ 4b ─▶ None
 ▲
dummy       return dummy.next
```

## Why it works

Each round takes the smallest remaining value, so the merged prefix is always sorted and never needs revisiting. When one list runs out, the other still holds a sorted run whose values are all at least as big as what has been merged, so attaching it whole is safe. Using `<=` means that on a tie the node from `list1` goes first, which keeps equal values in their original order.

## Where it goes wrong

Forgetting the leftover. The loop stops when either list is empty, not both, so the other list's tail would be dropped.

```text
list1: 1 ─▶ 2        list2: 5 ─▶ 6
loop ends after taking 1, 2 (list1 is None). Without the final link:
merged: 1 ─▶ 2 ─▶ None      5 and 6 are lost
```

Returning `dummy` instead of `dummy.next` includes the placeholder. When both lists are empty the loop never runs and `dummy.next` is `None`, which is the right answer.

## Cost

Time O(m + n): each node is attached once. Space O(1): only the `dummy` node and a few pointers; no node is copied.
