You are given `beginWord`, `endWord` and a list of distinct words `wordList`, all lowercase and of the same length. A transformation sequence changes exactly one letter per step, and every word after `beginWord` must be in `wordList`. `beginWord` itself does not have to be in the list.

Return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, counting both ends, or `0` if no sequence exists.

Constraints:
- `1 <= len(beginWord) <= 10`
- `1 <= len(wordList) <= 5000`
- `beginWord != endWord`
