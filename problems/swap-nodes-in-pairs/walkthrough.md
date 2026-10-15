## The idea

Swapping adjacent nodes means changing links, not values. For a pair `first → second`, three links must change: whoever points at `first` must now point at `second`, `second` must point at `first`, and `first` must point at what used to follow `second`. Do them in the wrong order and you lose part of the list.

The head changes after the first swap, which is a nuisance. A dummy node in front of the list removes the special case: the first pair is swapped like any other.

## Set-up

- `dummy` is a placeholder node whose `next` is `head`. At the end, `dummy.next` is the new head.
- `prev` is the node just before the pair being swapped. It starts at `dummy`. Invariant: everything up to and including `prev` is already finished.
- Each round names `first = prev.next` and `second = first.next`.
- The loop runs while two nodes remain after `prev`: `prev.next and prev.next.next`. A lone last node is left alone.

```text
dummy ──▶ 1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5 ──▶ None
 prev    first second
```

## Step by step

The three lines run in this order: `first.next = second.next`, `second.next = first`, `prev.next = second`.

```text
Round 1   first=1 second=2
  first.next = second.next    1 ──▶ 3
  second.next = first         2 ──▶ 1
  prev.next = second          dummy ──▶ 2

  dummy ──▶ 2 ──▶ 1 ──▶ 3 ──▶ 4 ──▶ 5
                  prev (now the old first)

Round 2   first=3 second=4
  3.next = 5,  4.next = 3,  1.next = 4

  dummy ──▶ 2 ──▶ 1 ──▶ 4 ──▶ 3 ──▶ 5 ──▶ None
                              prev

Check: prev.next is 5 and 5.next is None, only one node left. Stop.
```

Return `dummy.next`, which is `2`: the list `2 → 1 → 4 → 3 → 5`.

## Why it works

At the start of each round, the nodes up to `prev` are final and `prev.next` begins an untouched suffix. The three rewires swap the front two nodes of the suffix and leave the rest of it hanging off `first`. Because `first` is now the second node of the swapped pair, it is the next `prev`. Each round finishes two nodes, so the process ends when fewer than two remain.

## Where it goes wrong

Order matters. If `second.next = first` came first, the link from `second` to the rest of the list would be overwritten, and the nodes after the pair would be lost.

```text
Wrong:  second.next = first       2 ──▶ 1 ──▶ 2 ...   a cycle,
        first.next = second.next  and 3 is no longer reachable
```

Another slip is setting `prev = second`. The next pair starts after `first`, since `first` is now second in the pair.

Empty and one-node lists skip the loop because the loop test fails at once, and the function returns `dummy.next`, the original head.

## Cost

Time O(n): each node is touched once. Space O(1): a few references and the dummy.
