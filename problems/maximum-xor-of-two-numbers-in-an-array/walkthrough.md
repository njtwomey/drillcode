## The idea

Comparing every pair is O(n²). A better view: to maximise `x ^ y`, you want a 1 in the highest bit position possible, because one high bit outweighs every lower bit combined. So for each `x`, walk through the bits from the top and, at each position, pick a partner whose bit is the opposite of `x`'s whenever one exists.

To do that quickly, store all numbers in a binary trie, most significant bit first. Then "does a number exist with this prefix and this next bit?" is a single lookup.

## Set-up

- `bits` is `max(nums).bit_length()`. Higher positions are zero for every number, so they cannot matter.
- `root` is a trie where each node is a dict `{bit: child}`.
- Insert: for each number, walk from bit `bits - 1` down to 0 and `setdefault` the child for each bit.
- `best` holds the largest XOR found; `current` builds the XOR for one query.

## Step by step

Use `nums = [3, 5, 2, 6]`, so `bits = 3`. In binary: 3 = 011, 5 = 101, 2 = 010, 6 = 110.

```text
root
 ├─0─●─1─●─1   (3 = 011)
 │        └0   (2 = 010)
 └─1─●─0─●─1   (5 = 101)
       └1─●─0  (6 = 110)
```

Query `x = 5` (101):

```text
shift 2: bit 1, opposite 0 exists   current = 100   go to the 0 branch
shift 1: bit 0, opposite 1 exists   current = 110   go to child 1 (01x)
shift 0: bit 1, opposite 0 exists   current = 111   go to child 0 (010)
partner reached: 010 = 2           current = 7 = 5 ^ 2
```

Query `x = 3` (011):

```text
shift 2: bit 0, opposite 1 exists   current = 100   go to the 1 branch
shift 1: bit 1, opposite 0 exists   current = 110   go to child 0 (10x)
shift 0: bit 1, opposite 0 missing  current = 110   take child 1 (101)
current = 6 = 3 ^ 5
```

The other queries give at most 7, and 7 uses every possible bit, so the answer is 7.

## Why it works

The XOR is built from the top bit down. At each level, getting a 1 is worth more than all lower bits together, so taking the opposite child whenever it exists is never a mistake. If it does not exist, the bit must be 0 and we follow the only child there is. Since the walk always follows a path that was inserted, it ends at a real number from `nums`.

## Where it goes wrong

- Walking `bits` levels, not 32, is only valid because every number is padded to the same width; the loop must use the same `bits` for insert and query.
- When the opposite child is missing, you must take `node[bit]`; the child always exists because every inserted number has a full-length path.
- A single element pairs with itself, giving 0, which the code returns naturally.

## Cost

Time O(n * B) with B = bits per number (at most 31): each number is inserted and queried once. Space O(n * B) for trie nodes.
