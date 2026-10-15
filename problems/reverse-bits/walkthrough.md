## The idea

Reversing the bits of a 32-bit number means the lowest bit becomes the highest, the second lowest becomes the second highest, and so on. You can build the answer by reading bits off `n` from the bottom and pushing them onto the bottom of `result`. The first bit pushed gets shifted left the most times afterwards, so it ends up highest. That is a reversal.

Each round does two things: add `n`'s lowest bit to `result`, and drop that bit from `n`.

## Set-up

- `result` starts at 0 and collects the reversed bits.
- `n` is shifted right once per round so its next bit is at the bottom.
- The loop runs exactly 32 times.

Invariant: after `k` rounds, `result` holds the `k` lowest bits of the original `n`, in reverse order.

## Step by step

Wide numbers are hard to draw, so here is the same loop on 8 bits, using `n = 00010110`. The real code does exactly this for 32 rounds.

```text
round   bit taken   result after       n after
start               00000000           00010110
  1        0        00000000           00001011
  2        1        00000001           00000101
  3        1        00000011           00000010
  4        0        00000110           00000001
  5        1        00001101           00000000
  6        0        00011010           00000000
  7        0        00110100           00000000
  8        0        01101000           00000000
```

Each round first does `result << 1` (open a gap at the bottom), then ORs in the bit. The original reads `00010110`; the answer reads `01101000`, its mirror image.

For the real 32-bit input `43261596` the first 4 rounds look like this, as the low bits `0, 0, 1, 1` go in:

```text
n = 00000010100101000001111010011100
round 1: result = 0
round 2: result = 0
round 3: result = 1
round 4: result = 11
...
round 32: result = 00111001011110000010100101000000 = 964176192
```

## Why it works

A bit that is read in round `r` (counting from 1) is then shifted left by the remaining `32 - r` rounds. Original bit position `p = r - 1` therefore lands at position `32 - r = 31 - p`, which is exactly the mirror position.

## Where it goes wrong

Stopping early when `n` becomes 0, as you would in a bit-counting loop. The leading zeros of `n` must become trailing zeros of the answer, which only happens if the shifts keep going.

```text
8-bit example, n = 00000011
stop when n == 0 after 2 rounds:  result = 11        (should be 11000000)
run all 8 rounds:                 result = 11000000
```

## Cost

Time O(1): always 32 rounds. Space O(1): two integers.
