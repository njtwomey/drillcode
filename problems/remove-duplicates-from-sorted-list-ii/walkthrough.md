## The idea

Because the list is sorted, equal values sit together in runs. A value that is duplicated has a run longer than one node, and the whole run has to go, not just the extras. So walk the list run by run: a run of length one is kept, a longer run is cut out by re-pointing the node before it to the node after it.

To re-point, we need a handle on the last node we decided to keep, and for a duplicated head there is no such node. That is the job of a dummy node in front.

## Set-up

- `dummy` is a throwaway node whose `next` is `head`. It gives the head a predecessor, and `dummy.next` is the answer at the end.
- `prev` is the last node known to stay in the list. It starts at `dummy`.
- `curr` is the node being examined, starting at `head`.

The invariant: everything up to and including `prev` is final and has no duplicates; `prev.next` is where the next kept node will attach.

```text
dummy ──▶ 1 ──▶ 2 ──▶ 3 ──▶ 3 ──▶ 4 ──▶ 4 ──▶ 5 ──▶ None
 prev    curr
```

## Step by step

```text
curr=1: next is 2, different -> unique, prev = 1, curr = 2
curr=2: next is 3, different -> unique, prev = 2, curr = 3

curr=3: next is 3, same -> run. Slide curr to the last 3.
        prev.next = curr.next, skipping both 3s:

  dummy ─▶ 1 ─▶ 2 ──────────▶ 4 ─▶ 4 ─▶ 5
                prev   (3 ─▶ 3 cut out)
        prev stays at 2.  curr = curr.next = first 4

curr=4: next is 4, same -> run. Slide curr to the last 4.
        prev.next = 5:

  dummy ─▶ 1 ─▶ 2 ──────────────────▶ 5
                prev
        curr = 5

curr=5: next is None -> unique, prev = 5, curr = None. Stop.
```

`dummy.next` is `1 → 2 → 5`.

## Why it works

A run is dropped whole, so no copy of a duplicated value remains. A run of length one is untouched. Leaving `prev` where it is after a cut matters: the node after the run could itself begin another duplicated run, and `prev` must still be the node that gets re-pointed past it.

## Where it goes wrong

Moving `prev` forward after cutting a run is the classic slip. In the example, after the 3s are cut, putting `prev = curr` would set it to the second 3, which is no longer in the list, and the next cut would edit a detached node.

```text
wrong: after cutting 3,3 set prev = (second 3)
  list still reads ... 2 ─▶ 4 ─▶ 4 ─▶ 5
  the later cut changes the detached 3's next, so the 4s survive
```

Also without `dummy`, a duplicated head (like `1,1,2`) has no predecessor to adjust.

## Cost

Time O(n): `curr` only moves forward, and every node is touched a constant number of times. Space O(1): three references.
