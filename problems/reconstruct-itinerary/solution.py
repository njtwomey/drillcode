"""Reconstruct Itinerary (#332, hard)

Approach: Hierholzer's Eulerian path: DFS taking the smallest unused ticket, append
    airports in post-order, reverse at the end.
Tricks: Store destinations sorted in reverse so pop() is the smallest; a dead end is
    appended first so it lands last after the reversal.
Edge cases:
  - A smaller branch that is a dead end must be visited last
  - Several tickets between the same pair of airports
  - A single ticket

Time O(E log E), space O(E).
"""

from collections import defaultdict


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # Hierholzer's algorithm for an Eulerian path: every ticket is an edge that
        # must be used exactly once. Sort destinations in reverse so pop() from the
        # end of each list yields the lexically smallest remaining ticket in O(1).
        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)

        route = []

        def visit(airport):
            # Follow tickets greedily, smallest first. A destination with no tickets
            # left is a dead end; it can only be the final stop, and appending after
            # the recursion returns places it (and any stuck sub-trip) at the back.
            while graph[airport]:
                visit(graph[airport].pop())
            route.append(airport)

        visit("JFK")
        # Airports were appended in post-order, i.e. last stop first.
        return route[::-1]
