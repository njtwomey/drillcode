"""Monotonic stack of indices with decreasing temperatures.

Pop while today is warmer and record the index distance (store indices, not values).
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
