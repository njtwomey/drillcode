## The idea

For any bar, the biggest rectangle that uses that bar's full height stretches left and right until it meets a shorter bar. So the answer is the best over all bars of `height * width`, where the width is bounded by the nearest shorter bar on each side. Looking left and right from every bar costs O(n²).

A stack finds both boundaries in one pass. Keep a stack of bars with non-decreasing heights. A bar waits on the stack until a shorter bar arrives, which is the first moment we learn where its rectangle ends on the right. At that moment the left boundary is already known, because it is the bar beneath it on the stack.

## Set-up

- `bars` is `heights` with a `0` appended. The zero forces every remaining bar to be popped and measured at the end, with no separate clean-up loop.
- `stack` holds indices of bars with non-decreasing heights.
- `best` is the largest area seen so far.

When a bar is popped, its height is `height`. The new top of the stack is the nearest bar to its left that is not taller, because anything between was taller and has already been popped. So the rectangle starts at `left = stack[-1] + 1` (or 0 if the stack is empty) and ends at `i - 1`, giving width `i - left`.

```text
heights = [2, 1, 5, 6, 2, 3]  plus sentinel 0

index:    0  1  2  3  4  5  6
bars:     2  1  5  6  2  3  0
```

## Step by step

For each `i`, pop while the top is taller than `bar`, measure each pop, then push `i`.

```text
i=0  bar 2   stack empty                    push 0      stack [0]
i=1  bar 1   top is bar 2 > 1
             pop h=2, stack empty, left=0
             area = 2 * (1 - 0) = 2         best = 2
                                            push 1      stack [1]
i=2  bar 5   no pop                         push 2      stack [1, 2]
i=3  bar 6   no pop                         push 3      stack [1, 2, 3]
i=4  bar 2   top is bar 6 > 2
             pop h=6, top is index 2, left=3
             area = 6 * (4 - 3) = 6         best = 6
             top is bar 5 > 2
             pop h=5, top is index 1, left=2
             area = 5 * (4 - 2) = 10        best = 10
                                            push 4      stack [1, 4]
i=5  bar 3   no pop                         push 5      stack [1, 4, 5]
i=6  bar 0   pop h=3, top is index 4, left=5
             area = 3 * (6 - 5) = 3
             pop h=2, top is index 1, left=2
             area = 2 * (6 - 2) = 8
             pop h=1, stack empty, left=0
             area = 1 * (6 - 0) = 6         best stays 10
```

The best rectangle is height 5 over bars 2 and 3 (the 5 and the 6), area 10.

```text
        6
      5 █
      █ █
      █ █   3
 2    █ █ 2 █
 █ 1  █ █ █ █
 0 1  2 3 4 5       rectangle of height 5 covers indices 2..3
```

## Why it works

A bar is popped by the first bar to its right that is shorter, so `i` is its true right boundary. The bar left behind on the stack is the nearest shorter-or-equal bar on its left, so `left` is its true left boundary. Every bar is therefore measured with its exact widest rectangle, and the maximum over all bars is the answer. Note that bar 2 at index 4 reaches back to index 2 even though bars 5 and 6 sat there. Those taller bars were popped but the width they covered is inherited by the bar that popped them.

## Where it goes wrong

- Taking the left edge from the popped index instead of from the new top. Bars popped earlier were taller, and the current bar extends over them.
- Dropping the trailing `0`. Bars still on the stack would never be measured, and an increasing histogram like `[1, 2, 3, 4, 5]` would give 0.
- Using the wrong width when the stack is empty. The bar is the shortest so far, so its rectangle reaches back to index 0: `left = 0`.

## Cost

Time O(n): every index is pushed once and popped at most once. Space O(n) for the stack, in the worst case of strictly increasing heights.
