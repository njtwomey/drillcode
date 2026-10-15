"""Car Fleet (#853, medium)

Approach: Sort by position descending, compute each car's solo arrival time, and count a
    new fleet whenever a car arrives later than every fleet ahead.
Tricks: A car that would arrive earlier than the fleet ahead is capped to that fleet's
    time, so only strictly larger times start a fleet (ties merge).
Edge cases:
  - Single car
  - Equal speeds (no one ever catches up)
  - Two cars reaching the target at the same moment
  - Input positions not sorted

Time O(n log n), space O(n).
"""

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # Process cars from the one closest to the target backwards. A car can never pass
        # the one ahead, so if it would arrive no later than the fleet ahead, it catches
        # up and is slowed to that fleet's pace: same fleet. If it would arrive later,
        # nobody ahead can hold it back and it leads a new fleet.
        cars = sorted(zip(position, speed), reverse=True)
        fleets = 0
        slowest = 0.0  # arrival time of the nearest fleet ahead
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > slowest:
                fleets += 1
                slowest = time
        return fleets
