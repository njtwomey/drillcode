## The idea

Addition without `+` looks impossible until you notice what a column of binary addition does. In each bit position, two bits make a sum bit and a carry bit:

- The sum bit ignoring any incoming carry is `a XOR b`.
- The carry out is `a AND b`, and it belongs one position to the left, so it is `(a AND b) << 1`.

So `a + b = (a XOR b) + ((a AND b) << 1)`. That is still an addition, but the second term is now the carries only. Repeat: the carries get pushed further left each round until there are none, and what remains is the answer.

## Set-up

- `mask = 0xFFFFFFFF` keeps everything to 32 bits. Python integers have no fixed width, so a negative number would carry forever. Masking gives the two's complement view.
- `a &= mask` and `b &= mask` convert both inputs to that view.
- `a` is the partial sum without carries. `b` is the carries still to be added.
- Invariant: the true sum is always `a + b` (mod 2^32).

## Step by step

Add 5 and 3, shown with 4 bits for readability.

```text
              a      b      a XOR b   (a AND b) << 1
round 1     0101   0011      0110        0010
round 2     0110   0010      0100        0100
round 3     0100   0100      0000        1000
round 4     0000   1000      1000        0000   <- no carry left
```

Each round sets `a` to the XOR and `b` to the shifted AND. After round 4, `b` is 0 and `a = 1000`, which is 8.

## Why it works

XOR adds each column ignoring carries, and AND finds exactly the columns that generate a carry. Moving the carry one column left is just where it must be added. The total never changes, only the split between `a` and `b`. A carry moves at least one position up per round, so after at most 32 rounds it falls off the top and `b` becomes 0.

For negative results the final line handles the sign. If bit 31 is set, the 32-bit value is negative. `a ^ mask` flips the low 32 bits and `~` flips all the bits above, giving Python's negative integer.

```text
-1 + 0:  a = 0xFFFFFFFF   (bit 31 set, so negative)
         a ^ mask = 0,    ~0 = -1
```

## Where it goes wrong

- Skipping the mask. For a negative input Python's `a` and `b` have infinite sign bits, so `b` never reaches 0 and the loop does not finish.
- Masking the inputs but forgetting to mask inside the loop. The shifted carry grows past 32 bits.
- Returning `a` straight away. For a negative sum you would get a large positive number like `4294967295` instead of `-1`.

## Cost

Time O(1): at most 32 rounds, whatever the values. Space O(1).
