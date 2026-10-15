## The idea

Taking all the courses is possible exactly when the prerequisites contain no cycle. If A needs B, B needs C and C needs A, none of them can ever go first.

So we simulate taking courses. Any course with no unmet prerequisite can be taken now. Taking it satisfies one prerequisite of each course that depends on it, which may free more courses. If we run out of free courses before taking all of them, the leftovers are stuck on a cycle. This is Kahn's algorithm.

## Set-up

- `graph[p]` lists the courses that depend on `p`. Edges run from prerequisite to course.
- `indegree[c]` counts the prerequisites of `c` not yet satisfied.
- `queue` holds courses that are free to take. It starts with every course whose `indegree` is 0.
- `done` counts courses taken.

Invariant: a course is in `queue` only when its `indegree` has reached 0.

```text
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

graph:     0 ──▶ 1, 2
           1 ──▶ 3
           2 ──▶ 3
indegree = [0, 1, 1, 2]
queue    = [0]       done = 0
```

## Step by step

```text
take 0   done=1   indegree[1]: 1 -> 0  (queue it)
                  indegree[2]: 1 -> 0  (queue it)
         indegree = [0, 0, 0, 2]      queue = [1, 2]

take 1   done=2   indegree[3]: 2 -> 1
         indegree = [0, 0, 0, 1]      queue = [2]

take 2   done=3   indegree[3]: 1 -> 0  (queue it)
         indegree = [0, 0, 0, 0]      queue = [3]

take 3   done=4   no dependents       queue = []
```

`done == numCourses`, so the answer is `True`.

Now a cycle: 3 courses with `[[0,1],[1,2],[2,0]]`.

```text
indegree = [1, 1, 1]      queue = []     (nobody is free)
done = 0, which is not 3, so the answer is False.
```

## Why it works

A course reaches `indegree` 0 only after all its prerequisites have been taken. So the order we take courses in respects every prerequisite. If a cycle exists, each member waits on another member, so none reaches 0 and none is ever taken. If no cycle exists, there is always at least one course with no unmet prerequisite, so the queue never empties early.

## Where it goes wrong

Building the edge backward. The pair is `[course, prereq]`, and the edge must go `prereq -> course` so that `indegree[course]` rises. Swapping them still terminates but answers for the reversed graph, which has the same cycles, so a bug here can hide until you test ordering.

A self-dependency like `[a, a]` gives `a` an `indegree` of 1 that only `a` could clear, so it is never queued and the answer is `False`. Duplicate edges are fine because the count goes up and down once per copy.

## Cost

Time O(V + E): each course is queued once and each edge is relaxed once. Space O(V + E) for the graph, counts and queue.

## Other approaches

A DFS with three states per node (unvisited, in progress, done) also finds cycles: reaching an in-progress node means a cycle.
