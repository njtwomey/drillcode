"""Task Scheduler (#621, medium)

Approach: Count frequencies and compute (max - 1) * (n + 1) + number of tasks tied for
    max, floored at the task count.
Tricks: The most frequent task forces the frame layout; if other tasks overfill the gaps
    no idling is needed, hence the max with len(tasks).
Edge cases:
  - n = 0
  - Several tasks tied for the highest count
  - More distinct tasks than the cooldown

Time O(n), space O(1).
"""

from collections import Counter


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counts = Counter(tasks).values()
        most = max(counts)
        # How many task types are tied for the highest frequency.
        tied = sum(1 for c in counts if c == most)
        # The most frequent task fixes the skeleton: `most - 1` full frames of length
        # n + 1 (the task plus n cooling slots), then a last row holding one copy of
        # each tied task. Other tasks fit into the idle slots of the frames.
        frames = (most - 1) * (n + 1) + tied
        # If there are more tasks than the frames can hold, no idling is needed at
        # all and the answer is just the number of tasks.
        return max(len(tasks), frames)
