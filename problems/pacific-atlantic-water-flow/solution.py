"""Pacific Atlantic Water Flow (#417, medium)

Approach: DFS inward from each ocean's border cells, moving only to equal or higher
    cells; answer is the intersection.
Tricks: Reverse the flow: start from the oceans, not from every cell.
Edge cases:
  - Single row or column (every cell qualifies)
  - Plateau of equal heights

Time O(m·n), space O(m·n).
"""


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])

        # Flood uphill from the given border cells. Water flows downhill (or level)
        # from a cell to the ocean, so walking backwards we may only step to cells
        # that are >= the current one. Returns every cell that can reach this ocean.
        def reach(starts):
            seen = set(starts)  # border cells trivially touch their own ocean
            stack = list(starts)
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return seen

        # Pacific borders the top row and left column; Atlantic the bottom row and
        # right column. The ranges skip the shared corner so no cell is listed twice.
        pacific = [(0, c) for c in range(cols)] + [(r, 0) for r in range(1, rows)]
        atlantic = [(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows - 1)]
        # A cell qualifies only if both oceans reach it. Sorting just gives a
        # deterministic output order. Two searches of O(m*n) each: far cheaper than
        # a search from every cell, which would be O((m*n)^2).
        return [list(cell) for cell in sorted(reach(pacific) & reach(atlantic))]
