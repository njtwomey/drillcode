## The idea

We need an order of courses where every course comes after its prerequisites, or an empty list if that is impossible. That is a topological sort of a directed graph.

Think about which course you can take first: one with no prerequisites. Take it, and now every course that was waiting on it has one fewer thing to wait for. Whenever a course has nothing left to wait for, it is ready. Repeat. If you ever run out of ready courses before taking all of them, the leftovers wait on each other in a cycle.

## Set-up

- `graph[pre]` lists the courses that need `pre`. The edge points from prerequisite to dependant.
- `indegree[c]` counts the prerequisites of `c` not yet taken. It is the number of edges pointing into `c`.
- `queue` holds courses that are ready now (`indegree == 0`). It starts with every such course.
- `result` is the order built so far.

```text
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

graph:   0 ──▶ 1 ──▶ 3
         0 ──▶ 2 ──▶ 3

course     0  1  2  3
indegree   0  1  1  2
queue      [0]
result     []
```

## Step by step

```text
Pop 0.  result [0].  Courses 1 and 2 lose a prerequisite.
  indegree: 0  0  0  2      1 and 2 hit zero, so both join the queue
  queue [1, 2]

Pop 1.  result [0, 1].  Course 3 loses a prerequisite.
  indegree: 0  0  0  1      3 not ready yet
  queue [2]

Pop 2.  result [0, 1, 2].  Course 3 loses its last one.
  indegree: 0  0  0  0      3 joins the queue
  queue [3]

Pop 3.  result [0, 1, 2, 3].  Nothing depends on 3.
  queue []
```

`len(result) == numCourses`, so return `[0, 1, 2, 3]`.

## Why it works

A course enters the queue only after all its prerequisites have been appended to `result`, so every course in the output is preceded by what it needs. If there is no cycle, some course always has indegree zero, so the queue never gets stuck before the end.

## Where it goes wrong

Cycles. With `numCourses = 2` and `[[1,0],[0,1]]`:

```text
0 ──▶ 1 ──▶ 0

indegree   1  1       queue starts empty
result     []         length 0 != 2, return []
```

Courses on a cycle never reach indegree zero, so they never get ordered. The final length check is the only cycle detection needed. A self-prerequisite like `[0,0]` is the same thing. Duplicate pairs are fine because the edge and the indegree are counted the same number of times.

## Cost

Time O(V + E): each course is queued once and each edge is looked at once. Space O(V + E) for the graph and indegree array.
