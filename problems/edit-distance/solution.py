"""Edit Distance (#72, medium)

Approach: Table where dp[i][j] is the edit distance between the first i and first j
    characters; match copies the diagonal, else 1 plus the cheapest of replace, delete
    or insert.
Tricks: Initialise the first row and column to i and j (all inserts or all deletes), and
    index characters with i-1 and j-1 because the table is one larger.
Edge cases:
  - One or both strings empty
  - Identical strings (0)
  - Strings of different lengths

Time O(m·n), space O(m·n).
"""

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        # dp[i][j] = fewest edits to turn the first i characters of word1 into the first j
        # characters of word2.
        # Base cases: dp[i][0] = i (delete everything) and dp[0][j] = j (insert everything).
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Loop order: each cell reads its left, upper and upper-left neighbours, so plain
        # row-major order has them all ready.
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Last characters already agree: no edit needed for them.
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # One edit plus the cheapest way to line up what remains:
                    #   dp[i-1][j-1] replace, dp[i-1][j] delete from word1,
                    #   dp[i][j-1] insert into word1.
                    dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
