## The idea

If a list has a cycle, walking it never ends. Marking visited nodes in a set would catch that, at O(n) space. Floyd's idea needs only two pointers: one walking at speed 1 (`slow`) and one at speed 2 (`fast`). On a straight list, `fast` falls off the end. In a cycle, both circle round, and `fast` gains one node on `slow` every step, so it must eventually land on it, like a faster runner lapping a slower one on a track.

## Set-up

- `slow` and `fast` both start at `head`.

Invariant: `fast` is always at least as far along the list as `slow`. The loop condition `fast and fast.next` makes sure `fast.next.next` is safe to evaluate.

For the list `3 → 2 → 0 → -4`, where `-4` points back to `2`:

```text
   3 ──▶ 2 ──▶ 0 ──▶ -4
         ▲            │
         └────────────┘

 slow, fast both at 3
```

## Step by step

```text
Step 1   slow moves 1, fast moves 2
   slow at 2      fast at 0
Step 2
   slow at 0      fast at 2   (0 → -4 → 2)
Step 3
   slow at -4     fast at -4  (2 → 0 → -4)
   slow is fast, return True
```

Gap check, going forward from `slow` to `fast` around the cycle: the gap is 1 after step 1, 2 after step 2, and 3 after step 3, which is a full lap of this 3-node cycle, so it is 0. The gap grows by 1 per step, so it cannot jump over a lap.

A list with no cycle, `1 → 2`:

```text
start     slow = 1, fast = 1
step 1    slow = 2, fast = 1.next.next = None
loop test fast is None, exit, return False
```

## Why it works

Once both pointers are inside the cycle, the distance between them along the cycle changes by exactly 1 per step, so it cannot skip over the value that means "same node". In a list with no cycle, `fast` reaches `None` after about n/2 steps.

## Where it goes wrong

Comparing values instead of nodes. Different nodes can hold the same value, so use `is`:

```text
1 → 1 → 1 → None    (no cycle)
slow.val == fast.val would claim a cycle; slow is fast does not
```

And checking only `fast` for `None` crashes when `fast.next` is `None` on an odd-length list.

## Cost

Time O(n): `slow` takes at most about n steps before the pointers meet or `fast` ends. Space O(1): two references.
