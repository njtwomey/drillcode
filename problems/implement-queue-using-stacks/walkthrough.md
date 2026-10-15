## The idea

A queue is first in, first out; a stack is last in, first out. A stack on its own hands things back in the wrong order, but pouring one stack into another reverses it, and reversing a reversed order gives the original. So use two stacks: one to receive new items and one to serve old ones.

The cleverness is when to pour. Do it only when the serving stack is empty, and pour everything. Each item is then moved across at most once in its life, so the average cost per operation is constant.

## Set-up

- `in_stack` takes every `push`. Its top is the newest item.
- `out_stack` serves `pop` and `peek`. Its top is the oldest item.
- `_shift()` pours `in_stack` into `out_stack`, but only if `out_stack` is empty.

Invariant: reading `out_stack` from top to bottom and then `in_stack` from bottom to top gives the queue from front to back.

```text
in_stack  (top on right)   []
out_stack (top on right)   []
```

## Step by step

Operations: push 1, push 2, push 3, pop, push 4, pop, peek, pop, pop.

```text
push 1, 2, 3
  in_stack  [1, 2, 3]
  out_stack []

pop    out_stack empty, so shift:
  in_stack  []
  out_stack [3, 2, 1]        1 is on top now
  pop -> 1
  out_stack [3, 2]

push 4
  in_stack  [4]              goes behind 2 and 3
  out_stack [3, 2]

pop    out_stack not empty, no shift
  pop -> 2
  out_stack [3]

peek   no shift, top of out_stack -> 3

pop    -> 3
  out_stack []

pop    out_stack empty, shift:
  in_stack  []
  out_stack [4]
  pop -> 4
```

The order out was 1, 2, 3, 4, the same as the order in.

## Why it works

Popping from `in_stack` yields newest first, and pushing each onto `out_stack` flips it so the oldest ends on top. While `out_stack` still has items, everything in `in_stack` arrived later than all of them, so serving from `out_stack` first is correct.

## Where it goes wrong

Shifting while `out_stack` is not empty puts newer items underneath older ones, or under the wrong top, and breaks the order:

```text
out_stack [3, 2]   in_stack [4]
bad shift: out_stack [3, 2, 4]   -> pop returns 4 before 2
```

Also, `empty()` must check both stacks; items can be sitting in either.

## Cost

`push`, `empty` are O(1). `pop` and `peek` are O(1) amortised: one call can move many items, but each item is moved once, so n operations cost O(n) in total. Space O(n).
