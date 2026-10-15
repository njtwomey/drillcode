Each element of `asteroids` is an asteroid in a row: its absolute value is the size and its sign is the direction (positive moves right, negative moves left). All move at the same speed. When two collide the smaller one is destroyed, and if they are the same size both are destroyed. Asteroids moving the same way never meet, and asteroids that are moving apart never meet.

Return the asteroids that remain after all collisions have happened, in their original left-to-right order.

Constraints:
- `2 <= len(asteroids) <= 10^4`
- `-1000 <= asteroids[i] <= 1000`, and `asteroids[i] != 0`
