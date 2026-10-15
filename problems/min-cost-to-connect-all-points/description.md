`points` holds distinct integer coordinates `[x, y]` on a plane. Connecting two points costs their Manhattan distance, `|x1 - x2| + |y1 - y2|`.

Return the minimum total cost to connect all points so that there is exactly one simple path between any two of them.

Constraints:
- `1 <= len(points) <= 1000`
- `-10^6 <= x, y <= 10^6`
- All points are distinct.
