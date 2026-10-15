## The idea

A normal stack gives push, pop and top in O(1), but finding the minimum would mean scanning everything. The fix is to carry the answer along: when we push a value, also record the minimum of the stack at that moment. Because a stack only changes at its top, the minimum recorded with each entry stays correct for as long as that entry is the top.

## Set-up

- `stack` is a list of pairs `(value, min of the stack up to and including this entry)`.
- Invariant: for every entry, its second field equals the smallest value at or below it.

## Step by step

Operations: `push(-2)`, `push(0)`, `push(-3)`, `getMin()`, `pop()`, `top()`, `getMin()`.

```text
push(-2)    empty, so min is -2
            stack: [(-2,-2)]

push(0)     min(0, -2) = -2
            stack: [(-2,-2), (0,-2)]

push(-3)    min(-3, -2) = -3
            stack: [(-2,-2), (0,-2), (-3,-3)]

getMin()    top entry's second field  -> -3

pop()       remove (-3,-3)
            stack: [(-2,-2), (0,-2)]

top()       top entry's first field   -> 0

getMin()    top entry's second field  -> -2
```

The moment `-3` is removed, the minimum silently returns to `-2`, with no searching, because the entry below already remembered it.

```text
top ▶ (-3,-3)       after pop      top ▶ (0,-2)
      (0,-2)                             (-2,-2)
      (-2,-2)
```

## Why it works

The minimum of "everything at or below this entry" does not change while the entry is on the stack, since nothing below it can change without it being popped first. So the stored value is always right for the current top.

## Where it goes wrong

- When the stack is empty, there is no entry to compare with, so the first push uses `val` itself.
- A single global `min` variable fails on pop: if the minimum is removed, you would not know the next smallest. Storing the min per entry removes that problem.
- Duplicate minimums are handled for free, since each entry keeps its own copy.

## Other approaches

A second stack of minimums works too: push to it only when the value is `<=` the current min (the `<=`, not `<`, matters for duplicates), and pop from it when the popped value equals its top. It saves space when minimums are rare, at the cost of more care.

## Cost

Time O(1) for every operation. Space O(n), two numbers per entry.
