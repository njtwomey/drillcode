## The idea

Group the nodes at odd positions first, then the nodes at even positions, keeping their original order within each group. Positions, not values. Instead of building new nodes, rewire the existing ones: weave two chains through the list in a single pass, then glue the even chain after the odd chain.

## Set-up

- If the list has zero or one node, it is already grouped; return it.
- `odd` is the tail of the odd chain, starting at `head`.
- `even` is the tail of the even chain, starting at `head.next`.
- `even_head` remembers the first even node. Without it, once the chains split we would lose the start of the even group.

Invariant: `odd` and `even` are always adjacent pieces of the original list, `odd` right before `even`.

```text
odd even_head
 │   │
 1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5 ──▶ None
     even
```

## Step by step

The loop runs while `even and even.next`. Each round skips over one pair: `odd.next = even.next`, advance `odd`, then `even.next = odd.next`, advance `even`.

```text
Round 1   odd=1, even=2. even.next is 3.
  odd.next = 3     1 ──▶ 3
  odd = 3
  even.next = 4    2 ──▶ 4
  even = 4

  odd chain:   1 ──▶ 3 ──▶ 4 ──▶ 5       (tail of 3 still points at 4)
  even chain:  2 ──▶ 4 ──▶ 5

Round 2   odd=3, even=4. even.next is 5.
  odd.next = 5     3 ──▶ 5
  odd = 5
  even.next = None 4 ──▶ None
  even = None

  odd chain:   1 ──▶ 3 ──▶ 5 ──▶ None
  even chain:  2 ──▶ 4 ──▶ None
```

`even` is now `None`, so the loop ends. Finally `odd.next = even_head` joins them:

```text
1 ──▶ 3 ──▶ 5 ──▶ 2 ──▶ 4 ──▶ None
```

## Why it works

Every node is visited and relinked exactly once, and each round moves one odd and one even node into their chains in the original order. The last even node's `next` was set to what followed it, which is `None` at the end, so joining the chains does not create a cycle. Looping on `even and even.next` guarantees the nodes we point to exist.

## Where it goes wrong

- Losing `even_head`. Then after the loop there is no way to find where the even group starts.
- Checking only `odd.next` or only `even` in the loop condition. With an even-length list `even.next` is `None` after the last pair, and with `odd` checks you can dereference `None.next`.
- Forgetting that grouping is by position: `[8, 8, 1, 1, 8, 8]` becomes `[8, 1, 8, 8, 1, 8]`.

```text
two nodes: 1 ──▶ 2
  loop does not run (even.next is None)
  odd.next = even_head   1 ──▶ 2   unchanged, correct
```

## Cost

Time O(n): one pass. Space O(1): only `odd`, `even` and `even_head`.
