"""Flood Fill (#733, easy)

Approach: DFS or BFS from the start pixel, recolouring cells that match the original
    colour.
Tricks: Return early when the new colour equals the old one, otherwise the fill never
    terminates.
Edge cases:
  - Start pixel already the target colour
  - 1x1 image

Time O(m·n), space O(m·n).
"""


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        old = image[sr][sc]
        if old == color:
            return image
        stack = [(sr, sc)]
        image[sr][sc] = color
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < len(image) and 0 <= nc < len(image[0]) and image[nr][nc] == old:
                    image[nr][nc] = color
                    stack.append((nr, nc))
        return image
