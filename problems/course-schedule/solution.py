"""Course Schedule (#207, medium)

Approach: Kahn's algorithm: in-degree counts, repeatedly take zero-in-degree nodes; a
    cycle exists if not all are processed.
Tricks: DFS with three states (unvisited, in progress, done) also detects cycles.
Edge cases:
  - No prerequisites
  - Self-dependency [a, a]
  - Duplicate edges

Time O(V + E), space O(V + E).
"""
from collections import deque


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Edge prereq -> course. indegree[c] = prerequisites of c not yet satisfied.
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1
        # Courses with no unmet prerequisites can be taken right away.
        queue = deque(i for i in range(numCourses) if indegree[i] == 0)
        # Count courses taken. A cycle's members never reach indegree 0, so never get taken.
        done = 0
        while queue:
            node = queue.popleft()
            done += 1
            for nxt in graph[node]:
                # Taking this course satisfies one prerequisite of each dependent.
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        # Fewer than all taken means some courses are stuck waiting on a cycle.
        return done == numCourses
