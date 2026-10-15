You are given an array `stones` of positive integer weights. Repeatedly take the two heaviest stones and smash them together. If their weights are equal, both are destroyed. Otherwise the lighter one is destroyed and the heavier one is left with weight equal to the difference.

Continue until at most one stone remains. Return the weight of the remaining stone, or `0` if none remain.

Constraints:
- `1 <= len(stones) <= 30`
- `1 <= stones[i] <= 1000`
