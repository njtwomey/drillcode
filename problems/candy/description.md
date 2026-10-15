Children stand in a line, and child `i` has a rating `ratings[i]`. Hand out candies so that every child gets at least one, and any child with a strictly higher rating than an adjacent child gets strictly more candies than that neighbour. Children with equal ratings impose no constraint on each other.

Return the minimum total number of candies needed.

Constraints:
- `1 <= len(ratings) <= 2 * 10^4`
- `0 <= ratings[i] <= 2 * 10^4`
- O(n) time is expected
