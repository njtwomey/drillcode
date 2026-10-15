## The idea

Merging two sorted lists is easy: compare the two front nodes and take the smaller. With `k` lists the same idea works, but you need to find the smallest of `k` fronts each time. Scanning all `k` fronts costs O(k) per node, which is O(N * k) overall.

A min-heap fixes that. It holds only the current front node of each list, so the smallest front is always on top and costs O(log k) to get at. Pop it, append it to the output, then push the node that follows it in its own list. The heap never has more than `k` entries.

## Set-up

- `heap` holds tuples `(node.val, i, node)`, one per non-empty list. `i` is the list's index. Empty lists are skipped, which also covers `k = 0`.
- `dummy` and `tail` build the output. `tail` is the last node placed; `dummy.next` will be the head. The dummy means the first node needs no special case.
- The index `i` is a tiebreaker. When two values are equal, Python compares `i` next, so it never tries to compare two `ListNode` objects (which cannot be ordered).

```text
lists:  [0] 1 ──▶ 4 ──▶ 5
        [1] 1 ──▶ 3 ──▶ 4
        [2] 2 ──▶ 6

heap (value, list):  (1,0)  (1,1)  (2,2)
output: dummy
```

## Step by step

Each round: pop the smallest, link it after `tail`, push its successor if there is one.

```text
pop (1,0)  push (4,0)   heap: (1,1) (2,2) (4,0)      out: 1
pop (1,1)  push (3,1)   heap: (2,2) (3,1) (4,0)      out: 1 1
pop (2,2)  push (6,2)   heap: (3,1) (4,0) (6,2)      out: 1 1 2
pop (3,1)  push (4,1)   heap: (4,0) (4,1) (6,2)      out: 1 1 2 3
pop (4,0)  push (5,0)   heap: (4,1) (5,0) (6,2)      out: 1 1 2 3 4
pop (4,1)  no successor heap: (5,0) (6,2)            out: 1 1 2 3 4 4
pop (5,0)  no successor heap: (6,2)                  out: ... 4 4 5
pop (6,2)  no successor heap: empty                  out: ... 5 6
```

The two 4s tie on value, so `i` decides: list 0 comes out first. When the heap is empty the loop ends and `dummy.next` is the head of `1 → 1 → 2 → 3 → 4 → 4 → 5 → 6`.

## Why it works

Every list is sorted, so the smallest unplaced node overall must be the front of some list. The heap always contains exactly the front of each list that still has nodes, so its top is that smallest node. Taking it and exposing its successor keeps that true for the next round.

## Where it goes wrong

- Leaving out the index: `(node.val, node)` crashes with a `TypeError` as soon as two values tie.
- Pushing empty lists: `lists[i]` can be `None`, and `None.val` fails. The `if node` filter prevents it.
- Forgetting the successor push: the output would contain only `k` nodes.

## Cost

Time O(N log k), where N is the total node count: every node is pushed and popped once, each at O(log k). Space O(k) for the heap; the output reuses the existing nodes.

## Other approaches

Merge the lists pairwise, halving the number of lists each pass (divide and conquer). That is also O(N log k) time and needs no heap, and it uses O(1) extra space if done iteratively.
