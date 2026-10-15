## The idea

For each day we want the wait until a warmer day. The brute force scans forward from every day, which is O(n^2) when temperatures keep falling.

Flip the question. Walk the days once, keeping the days that are still waiting for something warmer. When a new day arrives that is warmer than some of them, it is the answer for exactly those days, and they can leave the waiting list. Each day joins the list once and leaves once.

## Set-up

- `answer` starts as all zeros. A day that never gets a warmer day keeps its 0.
- `stack` holds the indices of days still waiting. We store indices, not temperatures, because the answer is a distance `i - j`.

Invariant: the temperatures of the days on `stack` never increase from bottom to top. A new warm day pops everything colder than it off the top, so the top is always the coldest waiting day.

```text
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
index           0   1   2   3   4   5   6   7
stack = []      answer = [0, 0, 0, 0, 0, 0, 0, 0]
```

## Step by step

The stack is shown as indices, bottom on the left, with temperatures in brackets.

```text
i=0 (73)  nothing to pop.         stack = [0]
i=1 (74)  74 > 73: pop 0, answer[0] = 1.   stack = [1]
i=2 (75)  75 > 74: pop 1, answer[1] = 1.   stack = [2]
i=3 (71)  71 < 75: no pop.        stack = [2, 3]      (75, 71)
i=4 (69)  69 < 71: no pop.        stack = [2, 3, 4]   (75, 71, 69)
i=5 (72)  72 > 69: pop 4, answer[4] = 1
          72 > 71: pop 3, answer[3] = 2
          72 < 75: stop.          stack = [2, 5]      (75, 72)
i=6 (76)  76 > 72: pop 5, answer[5] = 1
          76 > 75: pop 2, answer[2] = 4
                                  stack = [6]
i=7 (73)  73 < 76: no pop.        stack = [6, 7]

answer = [1, 1, 4, 2, 1, 1, 0, 0]
```

Days 6 and 7 are still on the stack at the end, so their answers stay 0.

## Why it works

A day waits on the stack until the first later day that is strictly warmer. Because the stack is ordered by temperature, if today is not warmer than the top, it is not warmer than anything below it either, so the `while` loop can stop at the first failure. Every day popped at index `i` is popped by the first warmer day, which is exactly the answer we want.

## Where it goes wrong

Comparing with `<=` instead of `<`. Equal temperatures are not warmer, so a day with the same temperature must stay put and not pop.

Pushing values instead of indices loses the distance. And `answer[j] = i - j` uses the popped day `j`, not the top that remains.

## Cost

Time O(n): the inner `while` looks like a loop inside a loop, but each index is pushed once and popped at most once. Space O(n) for the stack in the worst case (a strictly falling run).
