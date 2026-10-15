## The idea

A tab's history is a list of pages plus a marker for which page you are on. Back and forward just move the marker. Visiting a new page throws away everything ahead of the marker and adds the new page after it.

You could use a stack for back and another for forward, but one list with an index is simpler and every operation is O(1).

## Set-up

- `self.history` is the list of pages in the order they were reached. Invariant: it holds the current page and every page behind and ahead of it that can still be reached.
- `self.curr` is the index of the page being shown. Invariant: `0 <= curr < len(history)`.

```text
BrowserHistory("leetcode.com")

 history: [leetcode.com]
           ^ curr = 0
```

## Step by step

```text
visit google, facebook, youtube
 history: [leetcode, google, facebook, youtube]
                                       ^ curr = 3

back(1)    curr = max(0, 3 - 1) = 2     -> facebook
back(1)    curr = max(0, 2 - 1) = 1     -> google
forward(1) curr = min(3, 1 + 1) = 2     -> facebook
```

Now the interesting one, `visit("linkedin")` from index 2 with youtube still ahead:

```text
before:  [leetcode, google, facebook, youtube]
                            ^ curr = 2

del history[curr + 1:]   [leetcode, google, facebook]
append linkedin          [leetcode, google, facebook, linkedin]
curr += 1                                             ^ curr = 3
```

The rest:

```text
forward(2)  curr = min(3, 3 + 2) = 3    -> linkedin   (nothing ahead)
back(2)     curr = max(0, 3 - 2) = 1    -> google
back(7)     curr = max(0, 1 - 7) = 0    -> leetcode   (clamped)
```

## Why it works

The list always represents a straight path through the pages with `curr` somewhere on it. Back and forward move along that path and `max` / `min` stop at its two ends. Visit cuts the path after `curr`, which is exactly the "forward history is cleared" rule, then extends it by one.

## Where it goes wrong

Forgetting to truncate on `visit` leaves dead forward pages. After going back and visiting a new page, `forward` could then reach a page from a different branch of history.

```text
no truncation, visit linkedin from index 2:
  history: [leetcode, google, facebook, youtube, linkedin]
  curr += 1 lands on index 3, which is youtube, not linkedin
```

The clamps matter too. `back(7)` without `max(0, ...)` would give index -6, which is out of range for this list. A smaller overshoot would silently wrap around to the end of the list.

## Cost

`back`, `forward` and `visit` are O(1) amortised: the slice deletion removes elements that were each added once. Space is O(number of visits).
