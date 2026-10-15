"""Daily Temperatures (#739, medium)

Approach: Stack of indices with decreasing temperatures; pop while the current day is
    warmer and record the distance.
Tricks: Store indices, not values, because the answer is a distance.
Edge cases:
  - Strictly decreasing input (all zeros)
  - Last element always 0

Time O(n), space O(n).
"""


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        # Indices of days still waiting for a warmer day. Their temperatures never increase
        # from bottom to top, so the top is always the coldest waiting day.
        stack = []
        for i, temp in enumerate(temperatures):
            # Today is the first warmer day for every colder waiting day. Each index is pushed
            # and popped once, so the inner loop is O(n) in total.
            while stack and temperatures[stack[-1]] < temp:
                j = stack.pop()
                answer[j] = i - j
            # Today now waits for its own warmer day. Never popped means answer stays 0.
            stack.append(i)
        return answer
