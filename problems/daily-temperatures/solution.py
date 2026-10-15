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
        stack = []
        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                j = stack.pop()
                answer[j] = i - j
            stack.append(i)
        return answer
