---
title: Design structures
area: Design
topics: [Design]
problems:
  - lru-cache
  - min-stack
  - implement-queue-using-stacks
  - find-median-from-data-stream
  - encode-and-decode-strings
  - implement-trie-prefix-tree
  - design-add-and-search-words-data-structure
  - lfu-cache
related: [dummy-head, heap-patterns, trie-patterns, stack-matching, fenwick-tree]
---
## Reach for it when

- The statement says "design a class" and lists several operations, each of which must be O(1) or O(log n).
- One structure gives fast lookup but no order, or order but slow lookup, and the problem needs both.
- The input is a sequence of operation calls rather than one array, so each call must be cheap and state must persist between calls.
- Data must be turned into a string and back with no loss.

## Setup

- Ask what each operation needs, then pick the structure that gives it for free. The answer is nearly always two structures working together, each covering what the other cannot.
- Constructor state: declare every structure in `__init__` with its invariant, written down before any method.
  - dict `entries` plus a doubly linked list with sentinels `head` and `tail`. Invariant: the dict holds exactly the nodes in the list, and the list is ordered newest at `head` to oldest at `tail`.
  - a stack of `(value, min so far)` pairs, or a stack plus a parallel min stack. Invariant: the second element is the minimum of everything at or below that entry.
  - `in_stack` and `out_stack`. Invariant: `out_stack` has the oldest element on top, and it is refilled only when empty.
  - `low` (max-heap) and `high` (min-heap). Invariant: every value in `low` is at most every value in `high`, and `len(low)` is `len(high)` or one more.
  - `values`, `freq` and `buckets` for frequency order. Invariant: `buckets[f]` is an `OrderedDict` of the keys used exactly `f` times, oldest first, and `min_freq` is the lowest non-empty `f`.
- Write small private helpers once (`_unlink`, `_push_front`, `_shift`) and build every public operation from them.
- Tests for these problems use the operations format: a list of method names with arguments, replayed against a fresh object.

## Template

```python
def make_cache(capacity):
    entries = {}
    head = {}
    tail = {}
    head["next"], tail["prev"] = tail, head

    def unlink(node):
        node["prev"]["next"] = node["next"]
        node["next"]["prev"] = node["prev"]

    def push_front(node):
        node["prev"], node["next"] = head, head["next"]
        head["next"]["prev"] = node
        head["next"] = node

    def get(key):
        node = entries.get(key)
        if node is None:
            return -1
        unlink(node)
        push_front(node)
        return node["value"]

    def put(key, value):
        node = entries.get(key)
        if node is not None:
            node["value"] = value
            unlink(node)
            push_front(node)
            return
        if len(entries) == capacity:
            oldest = tail["prev"]
            unlink(oldest)
            del entries[oldest["key"]]
        node = {"key": key, "value": value}
        entries[key] = node
        push_front(node)

    return get, put
```

After `get, put = make_cache(2)`, the calls `put(1, 1)`, `put(2, 2)`, `get(1)`, `put(3, 3)` leave `get(2)` at `-1` and `get(1)`, `get(3)` present. The closure stands in for a class; in a real answer, write a class.

## What it removes

- Linear scans for order. The dict finds a node in O(1) and the linked list moves it in O(1), so neither structure has to search the other.
- Null checks at the ends of the list. With sentinels, `_unlink` and `_push_front` are the same code for the first, last and only node.
- Recomputing a minimum or a median on demand. The extra structure maintains it as the data changes.
- Escaping rules for encoded strings. A length prefix means the decoder never inspects the payload.

## Pitfalls

- Updating an existing key in `put` without moving it to the front, or without refreshing its value. The wrong entry is evicted later.
- Evicting before checking whether the key already exists. Capacity 1 loses the entry just updated.
- Not storing the key in the list node. Eviction then cannot delete the dict entry.
- Popping a separate min stack out of step with the main stack, or pushing to it only on strictly smaller values. Duplicate minimums then pop the min too early. Storing `(value, min)` pairs avoids both.
- Refilling `out_stack` while it still holds items. Newer items go under older ones and order breaks. Refill only when empty, and make `empty()` check both stacks.
- Reading `peek` or `pop` without shifting first when `out_stack` is empty and `in_stack` is not.
- In `lfu-cache`, forgetting to move `min_freq` when `_touch` empties the lowest bucket, or to reset it to 1 when a new key is added. The next eviction then looks in an empty bucket and raises `KeyError`.
- In `lfu-cache`, accepting a `put` with capacity 0, or evicting before checking whether the key exists. Capacity 0 must store nothing; an existing key is a use, not a new entry.
- Splitting an encoded string on the delimiter. A string containing `#` breaks it. Read the length, then slice exactly that many characters.

## Variants

- Dict plus doubly linked list, `lru-cache`: dict for lookup, list for recency order, sentinels at both ends, `_unlink` and `_push_front` composed into `get` and `put`. Python's `OrderedDict` with `move_to_end` and `popitem(last=False)` does the same job in a few lines; use it only if the interviewer allows.
- Parallel state, `min-stack`: each entry stores `(value, current minimum)`, so `pop` restores the previous minimum without searching.
- Two stacks, `implement-queue-using-stacks`: push to `in_stack`, serve from `out_stack`, move across only when `out_stack` is empty. Each element moves at most once, so operations are amortised O(1).
- Two heaps, `find-median-from-data-stream`: max-heap for the lower half, min-heap for the upper, rebalanced after each add. See `heap-patterns`.
- Length-prefixed encoding, `encode-and-decode-strings`: write `len(s)#s` for each string. The decoder finds the first `#` after position `i`, reads the length, slices that many characters and jumps past them. Empty strings and strings containing `#` work.
- Tries as the data structure, `implement-trie-prefix-tree` and `design-add-and-search-words-data-structure`: the design is the trie itself. See `trie-patterns`.
- Frequency buckets, `lfu-cache`: three dicts, `values`, `freq` and `buckets`, where each bucket is an `OrderedDict` used as an ordered set. `_touch` moves a key from bucket `f` to `f + 1` and bumps `min_freq` only if it emptied bucket `min_freq`. Eviction is `buckets[min_freq].popitem(last=False)`, which gives least frequent, then least recent. Every operation is O(1).
- Prefix structure for updates, `range-sum-query-mutable`: a Fenwick tree. See `fenwick-tree`.
- Dict plus list with swap-and-pop gives constant-time insert, delete and random element. It is not in this catalogue.

## Worked example

Problem: `lru-cache`

A dict for lookup and a doubly linked list with dummy ends for recency order.

```python
class _Entry:

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.entries = {}
        self.head = _Entry()
        self.tail = _Entry()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, entry):
        entry.prev.next = entry.next
        entry.next.prev = entry.prev

    def _push_front(self, entry):
        entry.next = self.head.next
        entry.prev = self.head
        self.head.next.prev = entry
        self.head.next = entry

    def get(self, key: int) -> int:
        entry = self.entries.get(key)
        if entry is None:
            return -1
        self._unlink(entry)
        self._push_front(entry)
        return entry.value

    def put(self, key: int, value: int) -> None:
        entry = self.entries.get(key)
        if entry is not None:
            entry.value = value
            self._unlink(entry)
            self._push_front(entry)
            return
        if len(self.entries) == self.capacity:
            oldest = self.tail.prev
            self._unlink(oldest)
            del self.entries[oldest.key]
        entry = _Entry(key, value)
        self.entries[key] = entry
        self._push_front(entry)
```

`self.entries` is the dict and `self.head` and `self.tail` are the sentinels from Setup. Both `get` and `put` are built from `_unlink` and `_push_front` only. `put` handles the existing key first (update, refresh, return), then evicts `self.tail.prev` if the cache is full, which is why `_Entry` stores `key`. The dict and the list change together in every branch, which keeps their invariant.
