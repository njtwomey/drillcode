## The idea

We need every balanced string with `n` pairs of brackets. Generating all `2^(2n)` strings of `(` and `)` and filtering the valid ones is wasteful, because most are broken early (for example, starting with `)`).

Build strings one character at a time and only make moves that cannot go wrong. Two rules are enough:

- Add `(` while fewer than `n` have been used.
- Add `)` only while there is an unmatched `(` to close, that is, `closes < opens`.

Following those rules, every string you finish is balanced, so no filtering is needed. This is backtracking: add a character, explore, remove it, try the next choice.

## Set-up

- `path` is the string built so far, as a list of characters.
- `opens` and `closes` count how many of each are in `path`. They are the arguments of `dfs`.
- `result` collects finished strings.

Invariant: at every point, `closes <= opens <= n`, so the prefix is never invalid and can always be completed.

```text
n = 2

dfs(opens=0, closes=0)    path = ""
```

## Step by step

The recursion as a tree. Each line is a call, showing `path`. A branch that is not allowed is not shown.

```text
""                                 (0,0)  only "(" allowed: closes < opens is false
└─ "("                             (1,0)
   ├─ "(("                         (2,0)  opens == n, only ")" allowed
   │  └─ "(()"                     (2,1)
   │     └─ "(())"                 (2,2)  length 4: add to result
   └─ "()"                         (1,1)  closes == opens, only "(" allowed
      └─ "()("                     (2,1)
         └─ "()()"                 (2,2)  length 4: add to result

result = ["(())", "()()"]
```

At each call the code tries the open branch first, then, after undoing it with `path.pop()`, the close branch. That is why `"(("` comes before `"()"`.

## Why it works

The rule `closes < opens` means a `)` is only ever placed when it matches an earlier `(`, so the string never has more closes than opens in any prefix. The rule `opens < n` caps the opens. A string that reaches length `2n` therefore has `n` of each and never dipped below zero, which is the definition of balanced. Every balanced string is reachable, because each of its prefixes obeys both rules.

Every branch of the tree leads to at least one valid answer, so no work is wasted on dead ends.

## Where it goes wrong

Forgetting `path.pop()`. The same list is reused across branches, so each added character must be removed after the recursive call returns, or the next branch starts from a polluted path.

```text
no pop after the "(())" leaf -> path still reads "(())" when we return
to "(", so the next branch appends to "(())" instead of "(".
```

Checking `closes <= opens` instead of `<` lets a `)` be added with nothing to close, which produces `")("`.

## Cost

The number of results is the n-th Catalan number, about `4^n / (n * sqrt(n))`. Time is O(4^n / sqrt(n)) counting the work to build each string. Space O(n) for the recursion depth and `path`, excluding the output.
