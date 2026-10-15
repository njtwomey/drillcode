"""Boats to Save People (#881, medium)

Approach: Sort, then pair the heaviest remaining person with the lightest if they fit
    together, otherwise send the heaviest alone.
Tricks: The heaviest person needs a boat regardless, so the lightest is the best
    possible partner; check left <= right so a lone person is counted once.
Edge cases:
  - Single person
  - Nobody can share a boat
  - Odd number of people

Time O(n log n), space O(1).
"""

class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        # Each boat carries at most two people. The heaviest remaining person must take a
        # boat anyway, so pair them with the lightest one if that fits; if even the
        # lightest cannot join, nobody can, and the heavy person goes alone.
        people.sort()
        left, right = 0, len(people) - 1
        count = 0
        while left <= right:
            # Taking the lightest is safe whenever it fits; otherwise only right leaves.
            if people[left] + people[right] <= limit:
                left += 1
            right -= 1
            count += 1
        return count
