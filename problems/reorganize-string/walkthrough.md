## The idea

Two equal letters may not touch. The danger is a letter that is too common: with 4 characters, three copies of `a` cannot be separated (`a?a?a` needs 5 slots). In general a letter can appear at most `ceil(n / 2)` times, which is `(len(s) + 1) // 2`. If any letter exceeds that, return `""`. If none does, an arrangement always exists.

To build one, work with the two most frequent letters at a time. Placing two different letters side by side can never create a matching neighbour, and always spending the biggest piles keeps one letter from piling up at the end.

## Set-up

- `count` tallies each letter.
- `heap` is a max-heap of `(-count, letter)` pairs. Python's `heapq` is a min-heap, so counts are negated and the most frequent letter pops first.
- `result` is the output, built a pair at a time.

```text
s = "aaabbc"      n = 6, bound = (6 + 1) // 2 = 3, max count = 3, ok

heap (shown as count, letter):  (3,a)  (2,b)  (1,c)
result = []
```

## Step by step

Each round pops the top two letters, appends both, and pushes each back with one fewer copy if any remain.

```text
round 1  pop a(3), b(2)   result "ab"      push a(2), b(1)
         heap: a(2) b(1) c(1)

round 2  pop a(2), b(1)   result "abab"    push a(1), (b is spent)
         heap: a(1) c(1)

round 3  pop a(1), c(1)   result "ababac"  both spent
         heap: empty
```

Result `"ababac"`: no neighbours match. When the heap holds one letter at the end, it has one copy left and is appended on its own.

Impossible input: `"aaab"` has n = 4, bound 2, and `a` appears 3 times, so the answer is `""` straight away.

## Why it works

Each pair holds two different letters, so equal letters can only meet across a pair boundary. The second letter of one pair differs from the first of the next because the next pair starts with the most frequent letter, and the frequent one was just reduced. The bound check guarantees that when the heap shrinks to one letter, its count is at most 1, so it can be added at the end without touching a copy of itself.

## Where it goes wrong

- Skipping the bound check. `"aaab"` would pop `a` and `b`, then be left with `a(2)` alone. The code appends just one letter for the leftover, so it would return `"aba"`, which has lost a letter.
- Pushing a letter back with a zero count, which loops forever. The check `c1 + 1 < 0` (remember counts are negative) only pushes letters that still have copies.
- Popping only one letter per round. The same letter would be taken again and again, and neighbours could match.

## Cost

Time O(n log k) in general for k distinct letters. The alphabet is a fixed 26 letters, so the heap is tiny and the cost is O(n) in practice. Space O(1) beyond the output, bounded by the alphabet.
