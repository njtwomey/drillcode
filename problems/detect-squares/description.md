Design a class `DetectSquares` that stores points on a 2D plane and counts axis-aligned squares.

`add(point)` inserts the point `[x, y]` into the data structure. The same point may be added many times, and each copy is treated as a distinct point.

`count(point)` returns the number of ways to choose three stored points that together with the query point `[x, y]` form a square with positive area and sides parallel to the axes. Choices that use a different copy of a duplicated point are different ways. The query point itself is not added.

Constraints:
- `point.length == 2`
- `0 <= x, y <= 1000`
- At most `3000` calls to `add` and `count` combined
