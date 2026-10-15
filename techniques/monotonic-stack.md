---
title: Monotonic stack and deque
area: Stacks
topics: [Monotonic stack, Stack]
problems:
  - daily-temperatures
  - next-greater-element-ii
  - online-stock-span
  - largest-rectangle-in-histogram
  - remove-k-digits
  - car-fleet
  - sliding-window-maximum
related: [stack-matching, sliding-window, greedy-one-pass-invariants]
---
## Reach for it when
- The question is "next greater" or "next smaller" element.
- The wording is "how many days until".
- You need the maximum (or minimum) of every window of size `k`.
- A brute-force answer scans right from each position to find the first element that beats it.
- The array is circular, or the question is how far back the run of smaller values reaches ("span").
- You need the largest rectangle, where each bar's extent ends at the first shorter bar on each side.
- You must delete `k` digits to make the smallest number: a smaller digit should displace larger digits before it.

## Setup
- `stack = []`: indices of items still waiting for their answer. Invariant: their values are monotone, never increasing from bottom to top for "next greater".
- `for i, x in enumerate(a)`: today is `i`.
- `while stack and a[stack[-1]] < x`: pop `j = stack.pop()`. Index `i` is the answer for `j`, so record `i - j` (or `a[i]`).
- Then `stack.append(i)`.
- Store indices, not values, when the answer is a distance, a width or a window expiry. Store values (`remove-k-digits`) or `(price, span)` pairs (`online-stock-span`) when the position is not needed.
- The order depends on the question. "Next greater" keeps values non-increasing from bottom to top. "Largest rectangle" and "smallest number" keep them non-decreasing.
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
- Circular arrays: pushing indices on the second pass as well duplicates work. `next-greater-element-ii` pushes only while `i < n`.
- Largest rectangle without a trailing sentinel: bars still on the stack at the end are never measured. `heights + [0]` pops them all. `[1, 2, 3]` returns 0 without it.
- In `remove-k-digits`, forgetting that `k` may be left over (`"12345"`, `k = 2` pops nothing), so trim the end. Also strip leading zeros and return `"0"` for an empty result.
- In `car-fleet`, sorting ascending by position instead of descending: the comparison with the fleet ahead is then against the wrong neighbour.

## Variants
- Next greater, with distance (`daily-temperatures`): the template. Temperatures on the stack never increase from bottom to top, so the top is the coldest waiting day.
- Circular next greater (`next-greater-element-ii`): the loop runs `i` over `range(2 * n)` and reads `nums[i % n]`, so every element sees the whole circle. `result` is pre-filled with -1 and stores the greater value, not a distance. Indices are pushed only while `i < n`.
- Span (`online-stock-span`): a stream, so the stack lives on `self.stack` as `(price, span)` pairs. Popping every entry with price `<=` today's adds that entry's span to today's `span`, so a popped run is absorbed in one step. The stack keeps strictly decreasing prices.
- Largest rectangle (`largest-rectangle-in-histogram`): the stack holds indices of non-decreasing bars in `bars = heights + [0]`. A bar is popped when a shorter bar arrives, which fixes its right edge at `i`. Its left edge is `stack[-1] + 1` after the pop, or 0 if the stack is empty. The area is `height * (i - left)`, tracked in `best`.
- Smallest number after deleting digits (`remove-k-digits`): a stack of digit characters. While `k` is positive and the top is larger than the incoming `digit`, pop and decrement `k`. Leftover `k` trims the tail (`stack[:-k]`), because the stack is non-decreasing and the largest digits sit at the end.
- Sorted sweep, no stack (`car-fleet`): sort `(position, speed)` pairs from nearest the target, then compare each `time` with `slowest`, the arrival time of the fleet ahead. A larger time starts a new fleet. It is the same "only a blocker matters" idea, with the stack collapsed to one number because nothing is ever popped and re-read.
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
