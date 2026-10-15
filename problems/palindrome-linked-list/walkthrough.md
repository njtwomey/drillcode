## The idea

A palindrome reads the same from both ends. On an array you would run two pointers inward. A singly linked list cannot be walked backwards, so the usual shortcut is to copy the values into an array. That costs O(n) extra memory.

To do better, make the second half walkable from the tail by reversing it in place. Then compare the first half going forward with the reversed second half going forward. Three steps, each of which is a simple pattern you already know: find the middle with fast and slow pointers, reverse a list, compare two lists.

## Set-up

- `slow` and `fast` start at `head`; when `fast` runs out, `slow` is at the start of the second half.
- `prev` becomes the head of the reversed second half, and `nxt` holds the link we are about to overwrite.
- `left` walks the first half; `right` walks the reversed second half.

```text
head
 1 ──▶ 2 ──▶ 2 ──▶ 1 ──▶ None
 S,F
```

## Step by step

For `1 → 2 → 2 → 1`.

Phase 1, find the middle:

```text
Round 1   slow = 2 (first),  fast = 2 (second)
Round 2   fast.next exists, so slow = 2 (second), fast = None
          loop ends: slow is the first node of the second half
```

Phase 2, reverse from `slow` to the end (nodes `2 → 1`):

```text
before   1 ──▶ 2 ──▶ 2 ──▶ 1 ──▶ None
                     S

after    1 ──▶ 2 ──▶ 2 ◀── 1
                     │      ▲
                     ▼      prev (head of reversed half)
                    None
```

The first half still ends by pointing at the second `2`, but that node now points to `None`, so each half can be read without running into the other.

Phase 3, compare, with `left = head` and `right = prev`:

```text
Round 1   left = 1, right = 1   equal
Round 2   left = 2, right = 2   equal
right is None: stop, return True
```

## Why it works

The reversed half starts at the old tail, so walking it forward visits the second half's values in reverse order. The first half going forward and the second half going backward are exactly what a palindrome check compares. For an odd length such as `1 → 2 → 3 → 2 → 1`, `slow` stops on the middle `3`, which becomes the tail of the reversed part, so it ends up compared with itself and is harmlessly equal. The loop is on `right` because the reversed half is never longer than the first.

## Where it goes wrong

The loop condition for fast pointers must be `fast and fast.next`; checking only `fast.next` crashes on an empty list. Also remember the list is modified: the second half stays reversed unless you undo it, which is fine for this task but worth knowing.

A mismatch in the middle is caught the same way: `1 → 2 → 3 → 1`.

```text
slow stops at 3 (fast ran off), reversed half: 1 ─▶ 3
left = 1, right = 1  ok
left = 2, right = 3  differ, return False
```

## Cost

Time O(n): three linear passes. Space O(1): a handful of pointers, no copy of the values.
