`image` is a grid of integers. Starting from the pixel at row `sr`, column `sc`, recolor it and every pixel connected to it through 4-directional adjacency that shares its original color, setting each to `color`. Return the modified `image`.

Constraints:

- Grid dimensions are at most 50 x 50
- Diagonal neighbors are not connected
- `color` may equal the starting pixel's current color
