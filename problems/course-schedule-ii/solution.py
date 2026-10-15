"""Course Schedule II (#210, medium)

Approach: Kahn's topological sort: queue zero-in-degree courses and release dependants;
    fewer than n ordered means a cycle.
Tricks: Return the empty list when the order is shorter than numCourses; DFS post-order
    reversed also works.
Edge cases:
  - Cycle, including a self-prerequisite
  - No prerequisites
  - Duplicate pairs

Time O(V + E), space O(V + E).
"""

from collections import deque


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # Kahn's algorithm. indegree[c] counts the prerequisites of c still untaken;
        # a course with none left can be taken now.
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, pre in prerequisites:
            graph[pre].append(course)
            indegree[course] += 1
        queue = deque(c for c in range(numCourses) if indegree[c] == 0)
        result = []
        while queue:
            curr = queue.popleft()
            result.append(curr)
            # Taking curr satisfies one prerequisite of each course that follows it.
            for nxt in graph[curr]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        # Courses on a cycle never reach in-degree zero, so they never get ordered.
        return result if len(result) == numCourses else []
