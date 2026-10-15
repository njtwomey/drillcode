Build a class `UndergroundSystem` that records customer journeys and reports average travel times between stations.

- `checkIn(id, stationName, t)` records that the customer with card `id` entered `stationName` at time `t`. A card is checked in at only one station at a time.
- `checkOut(id, stationName, t)` records that the same customer left at `stationName` at time `t`.
- `getAverageTime(startStation, endStation)` returns the average duration of all completed journeys that began at `startStation` and ended at `endStation`.

Travel is directional, so the route from A to B is separate from B to A. Queries are only made for routes with at least one completed journey, and a card may be reused for later journeys.

Constraints:
- `1 <= id, t <= 10^6`
- At most `2 * 10^4` calls in total
