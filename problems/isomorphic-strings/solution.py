"""Isomorphic Strings (#205, easy)

Approach: Walk both strings together keeping a map in each direction; any contradiction
    means not isomorphic.
Tricks: One map is not enough, since two source chars may point at the same target;
    check both directions.
Edge cases:
  - Two source chars mapping to one target ("badc" / "baba")
  - One source char needing two targets
  - A character mapping to itself

Time O(n), space O(1).
"""

class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        # The mapping must be a bijection: one char of s -> one char of t, and no two
        # chars of s may share a target. Two dicts check both directions at once.
        s_to_t = {}
        t_to_s = {}
        for a, b in zip(s, t):
            # Either direction contradicting an earlier pairing breaks the rule, e.g.
            # "badc"/"baba" fails because b and d would both map to b.
            if s_to_t.get(a, b) != b or t_to_s.get(b, a) != a:
                return False
            s_to_t[a] = b
            t_to_s[b] = a
        return True
