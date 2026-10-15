"""Word Ladder (#127, hard)

Approach: BFS over words, finding neighbours through wildcard-pattern buckets such as
    h*t, with the step count as the level.
Tricks: Bucket words by pattern to avoid comparing every pair, and empty a bucket after
    its first expansion.
Edge cases:
  - End word not in the list
  - Begin word not in the list
  - End word in the list but unreachable

Time O(N * L²), space O(N * L²).
"""

from collections import defaultdict, deque


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        # Index every word under each wildcard pattern ("hot" -> "*ot", "h*t", "ho*").
        # Words sharing a pattern differ in exactly that one position, so a pattern
        # lookup finds all neighbours without comparing every pair of words.
        buckets = defaultdict(list)
        for word in words:
            for i in range(len(word)):
                buckets[word[:i] + "*" + word[i + 1:]].append(word)
        # BFS: the first time we pop endWord is along a shortest transformation.
        seen = {beginWord}
        queue = deque([(beginWord, 1)])
        while queue:
            curr, steps = queue.popleft()
            if curr == endWord:
                return steps
            for i in range(len(curr)):
                # Popping empties the bucket: every word in it is queued by now, so
                # visiting the same pattern again from another word would be wasted work.
                for nxt in buckets.pop(curr[:i] + "*" + curr[i + 1:], []):
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt, steps + 1))
        return 0
