## The idea

The question is how many bits of `n` are 1. The plain way checks all 32 positions one by one. A better way jumps straight from one set bit to the next, so the work is proportional to the number of 1s, not the width of the number.

The tool is `n & (n - 1)`. Subtracting 1 from a number flips its lowest 1 bit to 0 and turns every 0 below that bit into 1. Everything above is untouched. AND-ing that with the original therefore wipes out exactly the lowest set bit and nothing else.

## Set-up

- `count` starts at 0 and counts how many set bits we have removed.
- `n` is consumed: each round clears one bit.

Invariant: `count` plus the number of 1 bits still in `n` equals the original number of 1 bits. When `n` reaches 0, nothing is left to count.

## Step by step

Take `n = 11`, which is `1011` in binary.

```text
start        n = 1011   count = 0

round 1      n      = 1011
             n - 1  = 1010
             n & .. = 1010     lowest set bit (bit 0) cleared
             count  = 1

round 2      n      = 1010
             n - 1  = 1001     the borrow flipped bit 1 off and bit 0 on
             n & .. = 1000     bit 1 cleared
             count  = 2

round 3      n      = 1000
             n - 1  = 0111
             n & .. = 0000     bit 3 cleared, all the new 1s are masked off
             count  = 3
```

`n` is 0, so the loop stops and the answer is 3.

## Why it works

Write `n` as `[high bits] 1 [zeros]`, where the shown 1 is the lowest set bit. Then `n - 1` is `[high bits] 0 [ones]`. The high bits agree, so AND keeps them; the single position that was 1 is now 0; and the low positions were 0 in `n`, so AND gives 0 there. One bit is removed per pass, so the loop runs exactly as many times as there are 1s.

## Where it goes wrong

Shifting-based versions (`n >>= 1`) must run 32 times or until `n` is 0, and on a language with signed integers an all-ones input can loop forever with an arithmetic shift. The `n & (n - 1)` form avoids that: `n = 0` skips the loop and returns 0, and a value with all 32 bits set simply takes 32 rounds.

```text
n = 1111...1111 (32 ones)
each round clears the lowest 1, so 32 rounds
```

## Cost

Time O(k), where k is the number of set bits (at most 32, so O(1) in the worst case). Space O(1).
