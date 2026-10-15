"""Cheapest Flights Within K Stops (#787, medium)

Approach: Bellman-Ford limited to k + 1 rounds, relaxing every flight from a copy of the
    previous round's costs.
Tricks: Relax from a snapshot of the last round; updating in place lets one round chain
    several flights and ignores the stop limit.
Edge cases:
  - Cheapest path needs more stops than allowed
  - k = 0 allows only direct flights
  - Destination unreachable

Time O(k * E), space O(n).
"""

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int,
                          k: int) -> int:
        INF = float("inf")
        # Bellman-Ford limited to k + 1 edges (k stops means k + 1 flights). After
        # round i, cost[v] is the cheapest price to v using at most i flights.
        cost = [INF] * n
        cost[src] = 0
        for _ in range(k + 1):
            # Relax from a snapshot of the previous round. Relaxing in place would let
            # one round chain several flights and break the flight limit.
            nxt = cost[:]
            for u, v, price in flights:
                if cost[u] + price < nxt[v]:
                    nxt[v] = cost[u] + price
            cost = nxt
        return -1 if cost[dst] == INF else cost[dst]
