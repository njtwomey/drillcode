## The idea

The node to remove is `n` from the end, but a singly linked list only counts from the front. The obvious fix is two passes: count the length, then walk to position `length - n`. You can do it in one pass with two pointers held a fixed distance apart. When the leading pointer reaches the end, the trailing one is automatically at the right place, because it is the same distance from the end as the gap.

## Set-up

- `dummy` is a throwaway node in front of `head`. If the node to delete is the first one, it still has a predecessor, so no special case is needed.
- `fast` and `slow` both start at `dummy`.
- `fast` is first moved `n + 1` steps. The extra step makes the gap one larger than `n`, so when `fast` falls off the end, `slow` stops at the node before the one to delete, which is where we need to be to unlink it.

The invariant during the second loop: `fast` is always `n + 1` nodes ahead of `slow`.

```text
list 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5,  n = 2   (remove 4)

after opening the gap (3 steps):

 dummy ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None
 slow                fast
```

## Step by step

Move both pointers one node per round until `fast` is `None`.

```text
round 1   dummy ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None
                   slow             fast

round 2   dummy ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None
                         slow             fast

round 3   dummy ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None
                               slow             fast = None  (stop)
```

`slow` is at 3, just before 4. Run `slow.next = slow.next.next`:

```text
dummy ─▶ 1 ─▶ 2 ─▶ 3 ────────▶ 5 ─▶ None
                   slow    (4 is unlinked)
```

Return `dummy.next`, which is `1 → 2 → 3 → 5`.

## Why it works

The gap between the pointers is `n + 1` nodes, and `fast` ends at the position one past the tail. So `slow` is `n + 1` positions before that, which is exactly one before the `n`th node from the end. The distance never changes, so no length is needed.

## Where it goes wrong

- Opening the gap by `n` rather than `n + 1`. Then `slow` lands on the node to delete, and a singly linked list cannot unlink the node it is standing on.
- Returning `head`. If `n` equals the length, the head itself is removed.

```text
list 1 ─▶ 2, n = 2:  the head 1 is removed:
  dummy ────────▶ 2     return dummy.next = 2
                        (returning head would give the stale 1)
```

## Cost

Time O(L) for list length L: `fast` makes one pass in total. Space O(1): the dummy and two pointers.
