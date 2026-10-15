## The idea

Asteroids sit in a line. Positive numbers fly right, negative fly left, and the size is the absolute value. Two asteroids can only collide when a right-mover is somewhere to the left of a left-mover. Left-movers before right-movers fly apart, and same-direction asteroids never meet.

So when a new asteroid arrives, the only thing that matters is whether it is a left-mover and whether the nearest surviving asteroid on its left is a right-mover. "Nearest on the left" is the top of a stack.

## Set-up

- `stack` holds the survivors so far, in order. Invariant: no collision is pending among them. It may look like `[-3, -1, 4, 7]`: left-movers first, then right-movers.
- `alive` says whether the current `asteroid` is still intact while it fights.

```text
asteroids = [5, 10, -5, -12, 3]

stack: []        (reading left to right)
```

## Step by step

The `while` loop runs while the newcomer is negative, alive, and the top of the stack is positive.

```text
asteroid  5    not a left-mover, push          stack: [5]
asteroid 10    push                            stack: [5, 10]

asteroid -5    top 10 vs 5:  10 > 5, so the newcomer explodes
               alive = False, not pushed       stack: [5, 10]

asteroid -12   top 10 vs 12: 10 < 12, pop 10, newcomer survives
               top  5 vs 12:  5 < 12, pop 5,  newcomer survives
               stack is empty, loop stops
               alive, push                     stack: [-12]

asteroid  3    positive, push                  stack: [-12, 3]
```

The result is `[-12, 3]`. The `-12` and the `3` never meet because the `3` flies away to the right.

A tie, such as `[8, -8]`:

```text
asteroid  8    push                            stack: [8]
asteroid -8    top 8 == 8: pop it, alive = False
                                               stack: []
```

## Why it works

A newcomer can only collide with the survivor directly on its left. If it wins, that survivor is gone and the next one on the left is the new neighbour, so the loop repeats. If it loses or ties, it is gone and the stack below is untouched. Every asteroid is pushed at most once and popped at most once.

## Where it goes wrong

- Using `if` instead of `while` handles only one collision, so `-12` above would stop after killing `10` and wrongly leave `5` on the stack.
- Forgetting that equal sizes destroy both: the tie branch pops the top and also sets `alive = False`.
- Checking `stack[-1] > 0` matters. A negative top means the two are moving apart, so nothing happens and the newcomer is pushed.

## Cost

Time O(n): each asteroid is pushed once and popped at most once, even though the `while` is nested inside the `for`. Space O(n) for the stack.
