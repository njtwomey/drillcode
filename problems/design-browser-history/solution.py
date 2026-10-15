"""Design Browser History (#1472, medium)

Approach: A list of pages with a current index; visit truncates everything after the
    index.
Tricks: Clamp back and forward with max and min on the index; delete history[curr + 1:]
    on visit so stale forward pages disappear.
Edge cases:
  - back or forward by more steps than exist
  - visit after going back discards forward pages
  - Zero-step moves are not given but clamping must still hold

Time O(1) amortised per operation, space O(visits).
"""

class BrowserHistory:
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.curr = 0  # index of the page being shown

    def visit(self, url: str) -> None:
        # Visiting from the middle of the history discards the forward pages.
        del self.history[self.curr + 1:]
        self.history.append(url)
        self.curr += 1

    def back(self, steps: int) -> str:
        self.curr = max(0, self.curr - steps)  # clamp at the first page
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        self.curr = min(len(self.history) - 1, self.curr + steps)  # clamp at the last
        return self.history[self.curr]
