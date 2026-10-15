Cars drive along a one-lane road towards a destination at mile `target`. Car `i` starts at `position[i]` and travels at a constant `speed[i]`. A car cannot overtake: if it reaches the car in front it slows to that car's speed and they travel bumper to bumper as one fleet, and a fleet moves at the speed of its slowest member. A single car also counts as a fleet. Cars that meet exactly at the target are one fleet.

Return the number of distinct fleets that arrive at `target`.

Constraints:
- `1 <= len(position) == len(speed) <= 10^5`
- `0 <= position[i] < target <= 10^6`, with all positions distinct
- `1 <= speed[i] <= 10^6`
