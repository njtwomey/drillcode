There are `numCourses` courses labelled `0..numCourses - 1`. Each pair `[a, b]` in `prerequisites` means course `b` must be taken before course `a`.

Return an order in which all courses can be taken so every prerequisite comes first. If several orders work, any of them is accepted. If the prerequisites cannot all be satisfied, return an empty list.

Constraints:
- `1 <= numCourses <= 2000`
- `0 <= len(prerequisites) <= numCourses * (numCourses - 1)`
- All prerequisite pairs are distinct.
