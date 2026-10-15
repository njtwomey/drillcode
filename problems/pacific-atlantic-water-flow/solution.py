"""Reverse the flow: DFS inward from each ocean's border cells, moving only to
equal or higher cells. The answer is the intersection of the two reachable sets.

Time O(m*n), space O(m*n).
"""


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])

        def reach(starts):
            seen = set(starts)
            stack = list(starts)
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return seen

        pacific = [(0, c) for c in range(cols)] + [(r, 0) for r in range(1, rows)]
        atlantic = [(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows - 1)]
        return [list(cell) for cell in sorted(reach(pacific) & reach(atlantic))]
