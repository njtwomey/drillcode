## The idea

We need two things in O(1): find a key, and know which key was used longest ago. A hash map finds keys fast but has no usable order. A list can hold the order, but finding a node costs O(n). Together they work: the map points straight at the node in the list, and a doubly linked list lets you pull that node out of the middle and put it at the front in O(1).

## Set-up

- `entries` maps a key to its `_Entry` node.
- A doubly linked list holds the recency order. `head` is a dummy on the most-recently-used side, `tail` is a dummy on the least-recently-used side. The real nodes sit between them.
- Dummy ends mean `_unlink` and `_push_front` never check for "first" or "last".
- Each node stores its `key` as well as its `value`, so when we evict the node next to `tail` we can delete its dictionary entry.

```text
capacity 2, empty:

  entries = {}
  head ⇄ tail
```

## Step by step

```text
put(1, 1)   new key, room left, push to front
  entries = {1}
  head ⇄ [1] ⇄ tail

put(2, 2)   new key, room left
  entries = {1, 2}
  head ⇄ [2] ⇄ [1] ⇄ tail

get(1)      found; unlink it and push it to the front. returns 1
  entries = {1, 2}
  head ⇄ [1] ⇄ [2] ⇄ tail

put(3, 3)   new key, len(entries) == capacity
            oldest = tail.prev = [2]; unlink it; delete entries[2]
  entries = {1, 3}
  head ⇄ [3] ⇄ [1] ⇄ tail

get(2)      not in entries, returns -1
```

The `get(1)` is what saved key 1: without it, key 1 would have been the one next to `tail` and would have been evicted.

## Why it works

The list order is always most recent to least recent, because every use (a `get` hit, or a `put`) moves the touched node to the front, and the only removal is from the back. The node just before `tail` is therefore always the least recently used. The map and list stay in sync because every insert and delete updates both.

## Where it goes wrong

- A `put` on an existing key must update the value and move the node to the front, not add a second node, and it must not evict anything.
- Evict before inserting the new key, and only when the key is new.
- In `_push_front`, the order of the pointer writes matters. `head.next` must still be the old first node while you copy it to `entry.next` and fix its `prev`.

```text
Wrong: head.next = entry   (first)
       entry.next = head.next  -> points at itself, the old list is lost
```

## Other approaches

Python's `OrderedDict` with `move_to_end` and `popitem(last=False)` does the same job in a few lines. The hand-built list shows what it does internally.

## Cost

Time O(1) per `get` and `put`. Space O(capacity).
