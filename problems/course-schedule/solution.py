"""Kahn's algorithm: count in-degrees, repeatedly take zero-in-degree courses.

A cycle exists exactly when not every course gets processed.
Time O(V + E), space O(V + E).
"""
from collections import deque


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1
        queue = deque(i for i in range(numCourses) if indegree[i] == 0)
        done = 0
        while queue:
            node = queue.popleft()
            done += 1
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        return done == numCourses
