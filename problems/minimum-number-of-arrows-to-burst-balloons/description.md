Each balloon is a horizontal interval `points[i] = [x_start, x_end]` on a wall. An arrow shot vertically at coordinate `x` bursts every balloon with `x_start <= x <= x_end`, and keeps flying, so one arrow can pop many balloons.

Return the minimum number of arrows needed to burst all balloons. Balloons that merely touch at an endpoint can share an arrow.

Constraints:
- `1 <= len(points) <= 10^5`
- `-2^31 <= x_start < x_end <= 2^31 - 1` (fixed-width integers would overflow if you subtract)
