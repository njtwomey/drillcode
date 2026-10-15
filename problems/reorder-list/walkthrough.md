## The idea

The target order takes nodes alternately from the front and the back: first, last, second, second-last, and so on. A singly linked list cannot walk backwards, and copying nodes into an array would cost O(n) extra space. So rearrange the list itself in three moves:

1. Find the middle and split the list into two halves.
2. Reverse the second half, so its nodes can be read from the old tail forward.
3. Weave the two halves together, one node from each in turn.

## Set-up

- `slow` and `fast` find the middle. `fast` moves two nodes per step, `slow` one. The loop stops when `fast.next.next` is missing, so `slow` ends at the last node of the first half (the longer half when the length is odd).
- `second` begins as `slow.next`, the start of the back half. Then `slow.next = None` cuts the list so the first half really ends there.
- `prev`, `second` and `nxt` do an ordinary in-place reversal of the back half.

```text
1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None

stop: slow = 3, fast = 5
cut:  1 ─▶ 2 ─▶ 3 ─▶ None        second = 4 ─▶ 5 ─▶ None
```

## Step by step

Reverse the second half:

```text
4 ─▶ 5 ─▶ None     becomes     5 ─▶ 4 ─▶ None      (prev = 5)
```

Now weave. `first` starts at `head`, `second` at the reversed half. Each round saves both onward links, then points `first` at `second` and `second` at what `first` used to point to.

```text
start      first=1 ─▶ 2 ─▶ 3         second=5 ─▶ 4
round 1    save 2 and 4.  1 ─▶ 5 ─▶ 2 ─▶ 3        first=2, second=4
round 2    save 3 and None.  2 ─▶ 4 ─▶ 3          first=3, second=None  stop

result:  1 ─▶ 5 ─▶ 2 ─▶ 4 ─▶ 3 ─▶ None
```

Node 3 was the end of the first half, so its `next` was already `None`.

## Why it works

After the cut, the first half is at least as long as the reversed second half (equal for an even length, one more for an odd length). Every round consumes one node from each side, so the loop over `second` ends exactly when the back half is used up, and a single leftover first-half node is already in place at the end.

## Where it goes wrong

- Not cutting with `slow.next = None`. The first half would still point into the second half, and after reversing, the weave would create a cycle.

```text
no cut: node 3 still points at 4, and the weave sets 4.next = 3

  3 ─▶ 4 ─▶ 3 ─▶ 4 ...      a cycle, so any later traversal never ends
```

- Overwriting `first.next` before saving it. Both `first_next` and `second_next` must be saved before either link changes.
- Stopping on `fast.next` alone instead of `fast.next.next`, which moves `slow` one node too far for even lengths.

## Cost

Time O(n): the middle search, the reversal and the weave each touch each node once. Space O(1): a few pointers, and the work is done in place.
