## The idea

For each of `n` elements there are two choices: in the subset or out of it. That gives `2^n` subsets in total, and no shortcut can avoid listing them all, since that many results have to be produced.

The shortest way to list every combination of `n` yes/no choices is to count in binary. An `n`-bit number is exactly a row of `n` yes/no answers, and counting from 0 to `2^n - 1` visits every row once. Bit `i` of the mask says whether `nums[i]` is included.

## Set-up

- `n = len(nums)`.
- `mask` runs over `range(1 << n)`, which is `0 .. 2^n - 1`.
- For each mask the subset is `[nums[i] for i in range(n) if mask >> i & 1]`: shift bit `i` down to the lowest place and test it.

There is no loop state to maintain, only that every mask is a different subset.

```text
nums = [1, 2, 3]       bit 0 -> 1,  bit 1 -> 2,  bit 2 -> 3
```

## Step by step

Each mask picks out the elements whose bit is set. Bit 0 is the rightmost digit.

```text
mask  binary   bit2 bit1 bit0     subset
 0     000      .    .    .       []
 1     001      .    .    1       [1]
 2     010      .    2    .       [2]
 3     011      .    2    1       [1, 2]
 4     100      3    .    .       [3]
 5     101      3    .    1       [1, 3]
 6     110      3    2    .       [2, 3]
 7     111      3    2    1       [1, 2, 3]
```

Reading the subsets in order gives `[]`, `[1]`, `[2]`, `[1,2]`, `[3]`, `[1,3]`, `[2,3]`, `[1,2,3]`, which is the order the tests expect.

## Why it works

Distinct masks give distinct sets of included positions, and every set of positions is some mask, so each subset appears exactly once. Duplicate values are not an issue here because the elements are distinct by the problem statement. For an empty list, `1 << 0` is 1, so the only mask is 0, giving `[[]]`.

## Where it goes wrong

- Operator precedence in `mask >> i & 1`. Python reads it as `(mask >> i) & 1`, which is what we want. Writing `mask >> (i & 1)` would be a very different thing.
- Forgetting the empty subset or the full one by using the range `1 .. 2^n - 2`.

```text
n = 3: range(1 << 3) is 0..7  -> 8 subsets
       range(3)       is 0..2 -> only 3 masks, wrong
```

## Other approaches

The `subsetsDfs` variant decides one element at a time: skip `nums[i]` and recurse, then take it and recurse. When `i == len(nums)` the `path` is a finished subset and it is copied into `result`. After the take branch, `path.pop()` undoes the choice so the caller sees `path` unchanged.

```text
dfs(0) path=[]
  skip 1 -> dfs(1) path=[]
    skip 2 -> dfs(2) path=[]
      skip 3 -> record []
      take 3 -> record [3]
    take 2 -> ...
  take 1 -> dfs(1) path=[1] ...
```

Same output size and time. It uses O(n) recursion depth.

## Cost

Time O(n · 2^n): `2^n` masks, each scanning `n` bits. Space O(n) beyond the output, which itself holds `n · 2^n / 2` values.
