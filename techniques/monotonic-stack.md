---
title: Monotonic stack and deque
area: Stacks
topics: [Monotonic stack, Stack]
problems:
  - daily-temperatures
  - sliding-window-maximum
related: [stack-matching, sliding-window]
---
## Reach for it when
- The question is "next greater" or "next smaller" element.
- The wording is "how many days until".
- You need the maximum (or minimum) of every window of size `k`.
- A brute-force answer scans right from each position to find the first element that beats it.

## Setup
- `stack = []`: indices of items still waiting for their answer. Invariant: their values are monotone, never increasing from bottom to top for "next greater".
- `for i, x in enumerate(a)`: today is `i`.
- `while stack and a[stack[-1]] < x`: pop `j = stack.pop()`. Index `i` is the answer for `j`, so record `i - j` (or `a[i]`).
- Then `stack.append(i)`.
- Store indices, not values. The answer is usually a distance, and window expiry is a position check.
- `result` or `answer`: pre-filled with a default (0) for items that never get popped.

## Template
```python
def days_until_greater(a):
    answer = [0] * len(a)
    stack = []
    for i, x in enumerate(a):
        while stack and a[stack[-1]] < x:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
```

## What it removes
It removes the inner scan to the right from each position: O(n²) becomes O(n). Each index is pushed once and popped once, so the `while` loop costs O(n) in total even though it sits inside the `for`. For windows, the deque removes the O(k) maximum scan per window.

## Pitfalls
- Strict versus non-strict comparison when values repeat. In `daily-temperatures` the pop test is `<`, because an equal temperature is not warmer. In `sliding-window-maximum` it is `<=`, so an older equal value, which would expire first, is dropped.
- Forgetting to expire the front of the deque: a maximum from outside the window is reported.
- Reporting before the first full window: output starts at `i >= k - 1`, otherwise the result has `k - 1` extra entries.
- Storing values and then needing positions: the distance cannot be computed.
- Expecting every index to be answered: those never popped keep the default (0), so the pre-fill matters.

## Variants
- Next greater, with distance (`daily-temperatures`): the template. Temperatures on the stack never increase from bottom to top, so the top is the coldest waiting day.
- Window maximum (`sliding-window-maximum`): a `deque` named `queue` of indices with decreasing values. Pop from the back while the new value is `>=` the back's. Append `i`. If `queue[0] <= i - k`, `popleft()`. From `i >= k - 1`, `nums[queue[0]]` is the window maximum. The solution uses `if` for expiry, not `while`, because one index leaves per step. Only the front can be out of range, since indices increase.

## Worked example
Problem: `daily-temperatures`

Each day is the first warmer day for every colder day still waiting.

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        stack = []
        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                j = stack.pop()
                answer[j] = i - j
            stack.append(i)
        return answer
```

This is the template with `a` renamed. `stack` holds indices of days without a warmer day yet. The inner `while` pops each one that today beats and writes the gap `i - j`. Today is then pushed to wait for its own answer. A day never popped keeps its pre-filled 0.
