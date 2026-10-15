"""Design Hit Counter (#362, medium)

Approach: A deque of hit timestamps; on getHits evict those at or before timestamp minus
    300.
Tricks: Timestamps are non-decreasing so expired hits sit at the front and can be
    dropped for good; the window is timestamp-299..timestamp, so evict <= timestamp-300.
Edge cases:
  - Several hits in the same second
  - Query exactly 300 seconds after a hit (expired)
  - No hits yet

Time O(1) amortised per call, space O(hits in window).
"""

# Judge notes:
# Your HitCounter object will be instantiated and called as such:
# obj = HitCounter()
# obj.hit(timestamp)
# param_1 = obj.getHits(timestamp)


from collections import deque


class HitCounter:
    def __init__(self):
        self.window = deque()  # hit timestamps, oldest first (calls arrive in order)

    def hit(self, timestamp: int) -> None:
        self.window.append(timestamp)  # repeated timestamps are separate hits

    def getHits(self, timestamp: int) -> int:
        # The window is the 300 seconds timestamp-299 .. timestamp, so anything
        # at or before timestamp-300 is expired. Timestamps never go backwards,
        # so evicted hits can never be needed again.
        while self.window and self.window[0] <= timestamp - 300:
            self.window.popleft()
        return len(self.window)
