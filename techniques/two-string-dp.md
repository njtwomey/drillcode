---
title: Two-string DP
area: Dynamic programming
topics: [Dynamic programming, String]
problems:
  - longest-common-subsequence
  - edit-distance
  - distinct-subsequences
  - interleaving-string
  - longest-palindromic-subsequence
related: [dp-finding-the-state, dp-space-and-loop-order, expand-around-centre]
---
## Reach for it when
- The input is two strings (or one string and its reverse), and the question compares them: common subsequence, edit cost, how many times one spells the other.
- A third string must be built from the first two.
- Each step looks at the last character of a prefix of each string.
- A subsequence (not a substring) of one string is wanted, and the characters need not be adjacent.

## Setup
- `m, n`: the two lengths.
- `dp`: an `(m + 1) x (n + 1)` table. `dp[i][j]` is the answer for the prefixes `a[:i]` and `b[:j]`. The extra row and column are the empty prefixes.
- Characters are `a[i - 1]` and `b[j - 1]`, because the table is shifted by one.
- Base row and column: seed them from the meaning. Edit distance has `dp[i][0] = i` and `dp[0][j] = j`. Counting subsequences has `dp[i][0] = 1`. Longest common subsequence has zeros.
- Order: row-major. Each cell reads left, above and above-left, which are ready.
- Answer: `dp[m][n]`.

## Template
Longest common subsequence. The match case uses the diagonal; the other case keeps the better of dropping one character. It was run on small inputs.

```python
def table_over_prefixes(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# table_over_prefixes("abcde", "ace") == 3
```

## What it removes
- Trying every pairing of characters. Each cell is the answer for one pair of prefixes, and the recurrence only looks at the last characters.
- Backtracking over which characters to delete or keep. The three neighbours already hold those outcomes.
- Special cases for empty strings, since the zero row and column are the empty prefixes.

## Pitfalls
- Using `a[i]` instead of `a[i - 1]`. Symptom: IndexError at `i = m`, or the wrong characters compared.
- A wrong base row or column. `edit-distance` of `""` and `"abc"` must be 3, not 0. `distinct-subsequences` needs `dp[i][0] = 1`, otherwise every count is 0.
- Missing the "skip" term. In `distinct-subsequences`, `dp[i][j]` starts from `dp[i - 1][j]` (ways that never use `s[i - 1]`). The match adds `dp[i - 1][j - 1]` on top. Writing it as either/or loses counts, for example `"rabbbit"` to `"rabbit"` gives 3 only with both terms.
- Taking `min` over only the diagonal in `edit-distance`. A mismatch is one edit plus the cheapest of replace (`dp[i - 1][j - 1]`), delete (`dp[i - 1][j]`) and insert (`dp[i][j - 1]`).
- Early lengths check in `interleaving-string`. Without `m + n == len(s3)`, `s3[i + j - 1]` can go out of range or accept a wrong string.
- A greedy choice in `interleaving-string`. When `s1[i - 1] == s2[j - 1]`, either string may supply the character, so both must be tried.
- Confusing substring with subsequence in `longest-palindromic-subsequence`. A mismatch drops one end and keeps the better inside; it does not reset to 0.
- Wrong fill order for the interval table. `dp[i][j]` reads `dp[i + 1][j - 1]`, so `i` must run backwards. Running it forwards reads zeros.

## Variants
- Longest common subsequence: `longest-common-subsequence` takes the diagonal plus 1 on a match and the larger neighbour otherwise.
- Edit cost: `edit-distance` seeds `dp[i][0] = i` and `dp[0][j] = j`. A match copies the diagonal; a mismatch adds 1 to the minimum of three neighbours.
- Counting with match-or-skip: `distinct-subsequences` has `dp[i][j]` for `s[:i]` spelling `t[:j]`. It always copies `dp[i - 1][j]` and adds `dp[i - 1][j - 1]` when `s[i - 1] == t[j - 1]`.
- Two strings interleaving a third: `interleaving-string` has the cell `dp[i][j]` for `s3[:i + j]` built from `s1[:i]` and `s2[:j]`. `from_s1` needs `dp[i - 1][j]` and `s1[i - 1] == ch`; `from_s2` needs `dp[i][j - 1]` and `s2[j - 1] == ch`. The third string needs no index of its own, because its prefix length is `i + j`.
- One string, an interval table: `longest-palindromic-subsequence` does not compare with the reverse. It uses an `n x n` table where `dp[i][j]` covers `s[i..j]`. Equal ends give `dp[i + 1][j - 1] + 2`; otherwise `max(dp[i + 1][j], dp[i][j - 1])`. `i` runs from `n - 1` down and `j` from `i + 1` up. The reverse-and-LCS version is the same table in disguise.

## Worked example
Problem: `edit-distance`

The state is the cheapest edit count between the first `i` characters of `word1` and the first `j` of `word2`. The last character either already agrees or needs one of three edits.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

`m`, `n` and `dp` are the template's. The first row and column are the empty-prefix seeds. `word1[i - 1]` and `word2[j - 1]` are the shifted characters. The three terms in `min` are replace, delete and insert, read from the diagonal, above and left. The answer is `dp[m][n]`.
