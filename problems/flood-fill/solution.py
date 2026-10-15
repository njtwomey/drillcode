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
        # If the colours match, recolouring changes nothing and the "== old" check below
        # would keep re-matching, so cells would be pushed forever. Bail out early.
        if old == color:
            return image
        # Iterative DFS (explicit stack) avoids Python's recursion limit on big images.
        stack = [(sr, sc)]
        # Recolour when pushing (not when popping) so each cell is queued at most once.
        image[sr][sc] = color
        while stack:
            r, c = stack.pop()
            # Visit the 4 neighbours (no diagonals). Recoloured cells no longer equal old,
            # so the colour itself acts as the visited marker. Each cell is handled once.
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < len(image) and 0 <= nc < len(image[0]) and image[nr][nc] == old:
                    image[nr][nc] = color
                    stack.append((nr, nc))
        return image
