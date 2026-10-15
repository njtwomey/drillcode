## The idea

Copying `next` pointers alone is easy: build nodes front to back. The `random` pointers are the problem. A node's `random` can point forward or backward, and at the moment you create a copy, the copy of its target may not exist yet.

The fix is to separate creating from wiring. First make a new node for every old node and remember which is which in a dictionary. Then, with every copy in existence, translate each pointer through the dictionary.

## Set-up

- `copies` maps each old node to its new twin. It starts as `{None: None}`, so a null `next` or null `random` translates to null with no special case.
- `node` walks the original list.

Invariant after pass 1: every original node has exactly one copy, with the right value and no pointers yet.

```text
Original:  7 ──▶ 13 ──▶ 11 ──▶ None
           random:  7→None   13→7   11→13

copies = { None: None }
```

## Step by step

Pass 1 creates a bare copy of each node (shown with a prime).

```text
copies = { None: None,
           7:  7',
           13: 13',
           11: 11' }        (7', 13', 11' have next=None, random=None)
```

Pass 2 visits each original `node` and sets `copies[node].next = copies[node.next]` and likewise for `random`.

```text
node = 7    7'.next   = copies[13]   = 13'
            7'.random = copies[None] = None
node = 13   13'.next   = copies[11]  = 11'
            13'.random = copies[7]   = 7'      (points backward)
node = 11   11'.next   = copies[None] = None
            11'.random = copies[13]  = 13'

Result:    7' ──▶ 13' ──▶ 11' ──▶ None
           random:  7'→None   13'→7'   11'→13'
```

The function returns `copies[head]`, which is `7'`. For an empty list `head` is `None`, and the map hands back `None`.

## Why it works

After pass 1 the dictionary is a complete translation table from old nodes to new nodes. Pass 2 only ever points new nodes at new nodes, because every target is looked up in that table. Nothing in the copy touches an original node, so the two lists share no structure.

## Where it goes wrong

Trying to do everything in one pass. When you reach 7, its `random` target might be a node you have not copied yet, and you either lose it or create a duplicate.

Forgetting the `None` entry is the other slip: `copies[node.random]` would raise a `KeyError` for any node with a null pointer.

## Cost

Time O(n): two passes. Space O(n): the dictionary holds one entry per node, on top of the copy itself.

## Other approaches

The O(1) extra space version weaves each copy in right after its original (`7, 7', 13, 13', ...`), sets `random` via `node.random.next`, then unpicks the two lists. It avoids the map but is fiddlier to get right.
