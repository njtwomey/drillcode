Place `n` queens on an `n x n` chessboard so that no two queens attack each other: no two share a row, a column or a diagonal. Return every distinct arrangement.

Each arrangement is a list of `n` strings of length `n`, one per row, where `"Q"` marks a queen and `"."` an empty square. If no arrangement exists, return an empty list. The arrangements may be returned in any order.

Constraints:
- `1 <= n <= 9`
- Every solution must be listed, not just the first one found
