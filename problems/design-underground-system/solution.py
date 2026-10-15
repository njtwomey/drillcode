"""Design Underground System (#1396, medium)

Approach: A dict of open check-ins by id and a dict of (start, end) to total time and
    trip count.
Tricks: Store a running sum and count per route rather than every trip; the route key is
    ordered and the check-in is popped on checkout so ids can be reused.
Edge cases:
  - A to B and B to A are separate routes
  - Same customer id reused for a later journey
  - Several routes ending at the same station
  - Average that is not an integer

Time O(1) per operation, space O(open check-ins + routes).
"""

# Judge notes:
# Your UndergroundSystem object will be instantiated and called as such:
# obj = UndergroundSystem()
# obj.checkIn(id, stationName, t)
# obj.checkOut(id, stationName, t)
# param_1 = obj.getAverageTime(startStation, endStation)


class UndergroundSystem:
    def __init__(self):
        self.open = {}  # customer id -> (start station, check-in time)
        self.trips = {}  # (start, end) -> [total travel time, number of trips]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.open[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        # Removing the open check-in lets an id be reused for a later journey.
        start, began = self.open.pop(id)
        total = self.trips.setdefault((start, stationName), [0, 0])
        total[0] += t - began
        total[1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        # Keep only a sum and a count per route, not every trip, so this is O(1).
        # The key is ordered: A to B and B to A are different routes.
        total, count = self.trips[(startStation, endStation)]
        return total / count
