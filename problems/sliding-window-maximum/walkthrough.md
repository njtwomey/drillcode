## The idea

The brute force scans `k` values for every window position: O(n * k). But consecutive windows overlap almost completely, so most of that work is repeated.

The key observation: if a new number is bigger than an older number in the window, the older one can never be the maximum again. The new one is larger and leaves the window later. So older, smaller values can be thrown away the moment a bigger value arrives. What is left is a list that is decreasing from front to back, and its front is always the window maximum.

## Set-up

- `queue` is a deque of indices (not values) whose values are decreasing. Storing the index lets us tell when an entry has left the window.
- `result` collects one maximum per full window.

The invariant: `nums[queue[0]] > nums[queue[1]] > ...` and the indices increase from front to back, all inside the current window.

```text
nums  = [1, 3, -1, -3, 5, 3, 6, 7]     k = 3
index :  0  1   2   3  4  5  6  7

queue = []   (holds indices; shown below with their values)
```

## Step by step

Each round, pop smaller-or-equal values off the back, push `i`, drop the front if it is out of range (`queue[0] <= i - k`), and report once `i >= k - 1`.

```text
i=0  num=1   queue idx [0]       vals [1]
i=1  num=3   pop 1 (<= 3)
             queue idx [1]       vals [3]
i=2  num=-1  keep 3
             queue idx [1,2]     vals [3,-1]       report 3
i=3  num=-3  keep both
             queue idx [1,2,3]   vals [3,-1,-3]    report 3
i=4  num=5   pop -3, -1, 3; front 1 is also gone
             queue idx [4]       vals [5]          report 5
i=5  num=3   keep 5
             queue idx [4,5]     vals [5,3]        report 5
i=6  num=6   pop 3, 5
             queue idx [6]       vals [6]          report 6
i=7  num=7   pop 6
             queue idx [7]       vals [7]          report 7

result = [3, 3, 5, 5, 6, 7]
```

At `i=3` the window is indices 1..3 and the front, index 1, is still inside. Index 1 would expire at `i=4`, but by then `5` has already cleared it away.

## Why it works

An index is dropped from the back only when a later, at-least-as-large value exists, so it could never win again. An index is dropped from the front only when it has left the window. Everything else stays, in decreasing order, so the front is the largest value still in range. Only the front can expire, because indices are in increasing order.

## Where it goes wrong

- Storing values instead of indices: you cannot tell when the front has left the window.
- Popping with `<` instead of `<=` keeps duplicates, which is still correct but lets the deque hold equal values.
- Reporting before `i >= k - 1` would emit results for partial windows.

## Cost

Time O(n): each index is pushed once and popped at most once, so the inner `while` adds nothing on top of the loop. Space O(k) for the deque.
