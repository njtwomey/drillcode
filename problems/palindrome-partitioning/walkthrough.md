## The idea

We need every way to cut the string into pieces that are all palindromes. Build a partition left to right: choose the first piece, then choose the next piece from where it ended, and so on. Only try a piece if it is a palindrome. That prunes every branch that could never lead to a valid partition, and any path that reaches the end of the string is an answer.

This is backtracking: choose, explore, undo.

## Set-up

- `result`: the finished partitions.
- `path`: the pieces chosen so far in the current branch.
- `backtrack(start)`: pick the piece that begins at index `start`. Invariant: `path` is a list of palindromes that exactly covers `s[:start]`.
- The base case is `start == len(s)`: everything is covered, so copy `path[:]` into `result`.
- For each `end` from `start + 1` to `len(s)`, `piece = s[start:end]` is a candidate. If `piece != piece[::-1]` skip it.

```text
s = "aab"

path = []     start = 0
```

## Step by step

Each line is a call tree entry; indentation is recursion depth.

```text
backtrack(0)                          path = []
  end=1 piece "a"  palindrome         path = [a]
    backtrack(1)
      end=2 piece "a"  palindrome     path = [a, a]
        backtrack(2)
          end=3 piece "b"  palindrome path = [a, a, b]
            backtrack(3)              start == 3 -> record [a, a, b]
          pop "b"
        pop "a"
      end=3 piece "ab"  not a palindrome, skip
    pop "a"
  end=2 piece "aa"  palindrome        path = [aa]
    backtrack(2)
      end=3 piece "b"  palindrome     path = [aa, b]
        backtrack(3)                  start == 3 -> record [aa, b]
      pop "b"
    pop "aa"
  end=3 piece "aab"  not a palindrome, skip
```

The result is `[["a","a","b"], ["aa","b"]]`.

## Why it works

Every partition is a sequence of choices, each choosing where the next piece ends. The loop tries every possible end at every step, so every sequence is considered. The palindrome check removes only sequences that contain a bad piece. The `path.pop()` restores `path` to what it was, so the next sibling choice starts from the same state.

## Where it goes wrong

- Forgetting `path.pop()`. Pieces from the previous branch stay in `path` and results get polluted.
- Appending `path` rather than `path[:]`. The result would hold references to one list that later gets emptied.
- Starting `end` at `start` instead of `start + 1`, which tries an empty piece and loops forever.

```text
result.append(path)   instead of   result.append(path[:])

after the whole search, path = []:
  result = [[], []]     (both entries are the same emptied list)
```

## Cost

Time O(n * 2^n): there can be up to 2^(n-1) partitions (a string of one repeated letter), and each palindrome check and copy costs O(n). Space O(n) for the recursion depth and `path`, not counting the output.
