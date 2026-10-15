## The idea

Each digit independently chooses one of its letters, and a combination is one choice per digit. That is a tree: the first level picks the letter for digit 1, the second level picks for digit 2, and each leaf is a complete string. We just need to visit every leaf.

Backtracking does that naturally. Add a letter, recurse for the next digit, then remove the letter and try the next one. The number of results is the product of the letter counts, so there is no way to be faster than visiting them all.

## Set-up

- `mapping` is the keypad table. A table is clearer than arithmetic because 7 and 9 have four letters.
- `path` is the letters chosen so far, one per digit already decided.
- `result` collects finished strings.
- `dfs(i)` means "choose a letter for `digits[i]`". When `i == len(digits)`, every digit is decided and `path` is a full combination.
- An empty `digits` returns `[]` at the top, since the DFS would otherwise return `[""]`.

```text
digits = "23"      mapping: 2 -> abc    3 -> def
path = []          result = []
```

## Step by step

```text
dfs(0)  digit '2', letters a b c
 ├─ path=[a]  dfs(1)  digit '3', letters d e f
 │    ├─ path=[a,d]  dfs(2) -> record "ad"   pop d
 │    ├─ path=[a,e]  dfs(2) -> record "ae"   pop e
 │    └─ path=[a,f]  dfs(2) -> record "af"   pop f
 │   pop a
 ├─ path=[b]  dfs(1)
 │    ├─ "bd"
 │    ├─ "be"
 │    └─ "bf"
 │   pop b
 └─ path=[c]  dfs(1)
      ├─ "cd"
      ├─ "ce"
      └─ "cf"
```

The result is `["ad","ae","af","bd","be","bf","cd","ce","cf"]`.

Notice that `path` is the same list shared by every call. After recording "ad" and popping `d`, `path` is `[a]` again and ready for `e`.

## Why it works

At depth `i`, `path` holds a choice for each of the first `i` digits. Looping over every letter of `digits[i]` covers every option at that digit, and the `pop` restores the state so the next option starts from the same prefix. Every leaf is reached exactly once, and no two leaves are equal.

## Where it goes wrong

- Forgetting `path.pop()`. The letters pile up and the second branch starts from `[a, d]` instead of `[a]`.
- Appending `path` itself to `result`. It would append a reference to a list that keeps changing. `"".join(path)` makes a fresh string.
- Not guarding the empty input. Without the early return, `dfs(0)` hits the base case at once and returns `[""]`.

## Cost

Time O(4^n * n) for `n` digits: up to 4^n leaves, and joining each string costs O(n). Space O(n) for the recursion and `path`, not counting the output.
