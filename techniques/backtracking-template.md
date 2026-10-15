---
title: Backtracking template
area: Backtracking
topics: [Backtracking]
problems:
  - subsets
  - permutations
  - combination-sum
  - letter-combinations-of-a-phone-number
  - generate-parentheses
  - word-search
  - word-search-ii
related: [trie-patterns, bit-tricks, grid-traversal, dp-finding-the-state]
---
## Reach for it when

- The statement asks for all subsets, combinations, permutations or arrangements.
- It says "generate every valid ..." and the count of answers is exponential, so nothing can be counted by a formula.
- The task is a search in a grid for a word, where one path must not reuse a cell.
- Each answer is a sequence of choices and a partial sequence can be abandoned early.

## Setup

- `result = []`: the finished answers. Append a copy of `path`, never `path` itself.
- `path = []`: the choices made so far. Invariant: on entry to a call it holds exactly the decisions above this call, and on exit it is back to that same state.
- `start`, for subsets and combinations: the first index this call may choose from. Invariant: indices below `start` are never chosen again, so `[2, 3]` and `[3, 2]` are not both produced.
- `used`, for permutations: `used[i]` is true while `nums[i]` is in `path`. Invariant: it is set before the recursive call and cleared right after.
- An inner `def dfs(...)` closes over `result` and `path`, so only the state that changes per call (`start`, `remaining`, `i`, `opens`, `closes`) is passed as arguments.
- The loop body is always the same three lines: `path.append(choice)`, recurse, `path.pop()`.

## Template

```python
def backtrack_combinations(nums, target):
    nums = sorted(nums)
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            if nums[i] > remaining:
                break
            path.append(nums[i])
            backtrack(i + 1, remaining - nums[i])
            path.pop()

    backtrack(0, target)
    return result
```

This is combinations without reuse of an element and without duplicate answers, for input that may hold repeated values. `backtrack_combinations([10, 1, 2, 7, 6, 1, 5], 8)` gives `[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]`. The Variants section says what to change for the other shapes.

## What it removes

- Hand-written nested loops of unknown depth: recursion supplies one loop level per decision.
- Building and copying a new list at every call. One shared `path` is extended and shortened in place, so each step costs O(1) apart from the copy at a leaf.
- Post-filtering. Pruning inside the loop (`break` on a negative remainder, the parenthesis rules) stops a branch before it grows, so no invalid candidate is generated and then thrown away.

## Pitfalls

- Appending `path` instead of `path[:]`. Every entry of `result` ends up as the same list and prints as empty `[]` after the search unwinds.
- Not undoing a choice after the recursive call. Later siblings start from a polluted state and answers have extra elements or are missing.
- Passing `start` where the recursion needs `i + 1`. An element is reused when it should not be, for example `[1, 1]` from a single `1`.
- Passing `i + 1` where reuse is allowed. Combination sum then misses `[2, 2, 3]` for target 7.
- Recursing with a start index in letter combinations. There the recursion index is the digit position and advances by one per call; looping over later digits' letters produces wrong strings.
- Skipping duplicates with `nums[i] == nums[i - 1]` without sorting first, or with `i > 0` instead of `i > start`. The first form lets duplicate answers through; the second also drops `[1, 1, 6]` because the second `1` is never allowed at depth two.
- `break` where `continue` is needed. `break` is only correct when the candidates are sorted and every later one is at least as large.
- Returning `[""]` for empty input in letter combinations when the problem wants `[]`.

## Variants

- Subsets, `subsets`: record at every call, or decide each element in or out (`dfs(i + 1)` once without it, once with it) and record when `i == len(nums)`. The second form is what the solution's `subsetsDfs` does. The solution's main method instead counts a bitmask from 0 to `2^n - 1`, see `bit-tricks`.
- Permutations, `permutations`: no `start`. Loop over every index from 0, skip those with `used[i]` set, record when `len(path) == len(nums)`. Swapping elements in place is the alternative that avoids `used`, but this catalogue's solution uses `used`.
- Combinations with reuse, `combination-sum`: recurse with `i` instead of `i + 1`, sort the candidates once and `break` as soon as a candidate exceeds `remaining`.
- Digit positions, `letter-combinations-of-a-phone-number`: the recursion index is the position in `digits`; each call loops over the letters of that one digit, never over later digits. A mapping table handles digits 7 and 9, which have four letters.
- Constraint as the choice rule, `generate-parentheses`: no loop at all. Two guarded branches, `(` while `opens < n` and `)` while `closes < opens`. These two rules make every leaf valid, so no stack or final check is needed.
- Grid, `word-search`: the choice is a neighbouring cell. Overwrite the cell with `"#"` before recursing and restore the saved letter afterwards. The mark replaces a visited set, and the letter test rejects marked cells for free. Return a boolean with `or` so the search stops at the first success.
- Trie-guided grid, `word-search-ii`: the recursion also carries the current trie node and only enters a neighbour whose letter is a child. The end marker is popped when a word is found, and exhausted branches are deleted. See `trie-patterns`.

## Worked example

Problem: `combination-sum`

Sorted candidates, `start` as the lower bound of the loop, and reuse by recursing with `i`.

```python
class Solution:

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates = sorted(candidates)
        result = []
        path = []

        def dfs(start, remaining):
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                if c > remaining:
                    break
                path.append(c)
                dfs(i, remaining - c)
                path.pop()
        dfs(0, target)
        return result
```

`result` and `path` are declared before the inner `dfs`, which is the template's `backtrack`. `start` bounds the loop. `remaining` plays the role of the target and doubles as the pruning test, so `break` ends the loop once a sorted candidate is too large. The recursive call passes `i`, not `i + 1`, which is the difference from the template's no-reuse rule. The candidates are distinct in this problem, so the duplicate-skip line is not needed. `path.pop()` follows every recursive call.
