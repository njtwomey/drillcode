## The idea

The answer for index `i` is everything to its left multiplied by everything to its right. The tempting shortcut, the total product divided by `nums[i]`, fails when there are zeros (and is banned anyway).

So compute the two halves separately. One pass left to right collects the product of everything before each index. A second pass right to left multiplies in the product of everything after it. Neither half ever includes `nums[i]` itself.

## Set-up

- `result` is the output array, all 1s at first. It doubles as storage for the left products, so no extra array is needed.
- `prefix` is a running product of the elements already passed in the forward pass.
- `suffix` is the same, for the backward pass.

The invariant: when we write `result[i]` in a pass, the running product holds only elements on one side of `i`.

```text
nums   = [1, 2, 3, 4]
result = [1, 1, 1, 1]
prefix = 1
```

## Step by step

Pass 1: write `prefix` into `result[i]` first, then fold in `nums[i]`.

```text
i=0  result[0] = 1     prefix = 1*1 = 1
i=1  result[1] = 1     prefix = 1*2 = 2
i=2  result[2] = 2     prefix = 2*3 = 6
i=3  result[3] = 6     prefix = 6*4 = 24

result = [1, 1, 2, 6]       (product of everything to the left)
```

Pass 2: go backwards, multiply `result[i]` by `suffix`, then fold in `nums[i]`.

```text
i=3  result[3] = 6*1  = 6     suffix = 1*4  = 4
i=2  result[2] = 2*4  = 8     suffix = 4*3  = 12
i=1  result[1] = 1*12 = 12    suffix = 12*2 = 24
i=0  result[0] = 1*24 = 24    suffix = 24*1 = 24

result = [24, 12, 8, 6]
```

## Why it works

After pass 1, `result[i]` is the product of `nums[0..i-1]`. In pass 2, `suffix` at index `i` is the product of `nums[i+1..]`. Multiplying gives every element except `nums[i]`. Zeros need no special case because we never divide: a zero just makes the products that include it zero, which is the right answer.

## Where it goes wrong

The order inside each loop matters. If you fold `nums[i]` into the running product before writing it, `nums[i]` ends up in its own answer.

```text
Wrong:  prefix *= nums[i]; result[i] = prefix
  result after pass 1 = [1, 2, 6, 24]   (each includes itself)
```

## Cost

Time O(n): two passes. Space O(1) beyond the output, since the left products live in `result` and `suffix` is one variable.
