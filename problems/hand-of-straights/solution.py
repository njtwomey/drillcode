"""Hand of Straights (#846, medium)

Approach: Count the cards, then walk values in ascending order and consume a run of
    groupSize consecutive values starting at each smallest remaining card.
Tricks: Check len(hand) % groupSize first; when several copies of a card remain, all of
    them must start runs, so subtract the full count at once.
Edge cases:
  - Length not divisible by groupSize
  - groupSize of 1
  - Gap in the values
  - Duplicates that start overlapping runs

Time O(n log n), space O(n).
"""

from collections import Counter


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        # Every card belongs to exactly one group, so the sizes must divide evenly.
        if len(hand) % groupSize:
            return False
        count = Counter(hand)
        # Greedy: the smallest remaining card can only be the start of its group (nothing
        # smaller is left to extend it downward), so build a run from it right away.
        for card in sorted(count):
            need = count[card]  # runs that must start at this card
            if need == 0:
                continue  # all copies were already used by runs started earlier
            for val in range(card, card + groupSize):
                # Lookups on a Counter do not insert missing keys, so a gap reads as 0.
                if count[val] < need:
                    return False
                count[val] -= need
        return True
