Implement a class `BrowserHistory` that models a single browser tab.

`BrowserHistory(homepage)` starts the tab on `homepage`. `visit(url)` navigates to `url` from the current page and clears all forward history. `back(steps)` moves back up to `steps` pages and returns the URL now shown; if there are fewer than `steps` pages behind, it stops at the earliest page. `forward(steps)` is the mirror image and stops at the most recent page ahead.

Constraints:
- `1 <= steps <= 100`
- URLs are lowercase strings of length 1 to 20
- At most `5000` calls in total
