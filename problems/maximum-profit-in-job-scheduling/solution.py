"""Maximum Profit in Job Scheduling (#1235, hard)

Approach: Sort jobs by end time, then best[k] is the top profit over the first k jobs,
    found by skipping a job or taking it after the prefix located by bisect.
Tricks: Use bisect_right on the end times so a job may start exactly when another ends;
    sorting by end makes compatible earlier jobs a prefix.
Edge cases:
  - Jobs that touch at a boundary are compatible
  - One high-profit job spanning many small ones
  - Jobs with the same end time
  - Unsorted input

Time O(n log n), space O(n).
"""

from bisect import bisect_right


class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        # Sort jobs by end time. Then "the jobs that finish before this one starts" is
        # always a prefix of the sorted order, which is what makes the DP linear.
        jobs = sorted(zip(endTime, startTime, profit))
        # best[k] = max profit using only the first k jobs in sorted order.
        best = [0]
        ends = []  # end times of the jobs already processed, ascending
        for end, start, gain in jobs:
            # Number of earlier jobs with end <= start. bisect_right (not _left) lets a
            # job begin exactly when another ends, as the problem allows.
            k = bisect_right(ends, start)
            # Either skip this job (keep the best so far) or take it on top of the best
            # schedule that fits entirely before it.
            best.append(max(best[-1], best[k] + gain))
            ends.append(end)
        return best[-1]
