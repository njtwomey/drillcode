## The idea

This is schoolbook addition of `1`. Start at the least significant digit. If it is below 9, add one and you are done: nothing to its left changes. If it is a 9, it becomes 0 and a carry moves one place left.

The carry can only keep travelling through 9s. So the loop stops at the first digit that is not 9. The one case where it never stops is a number made entirely of 9s, which needs one more digit than it started with.

## Set-up

There is almost nothing to declare. The loop index `i` starts at the last position and moves left. The array itself is the state: digits to the right of `i` have already been turned into 0s by the carry, and digits to the left are untouched.

```text
digits  [1, 9, 9]
         0  1  2
               ^ i
```

## Step by step

Take `[1, 9, 9]`, which should become `[2, 0, 0]`.

```text
i = 2   digits[2] is 9, not below 9
        write 0, carry moves on

        [1, 9, 0]
            ^ i next

i = 1   digits[1] is 9
        write 0, carry moves on

        [1, 0, 0]
         ^ i next

i = 0   digits[0] is 1, below 9
        add one and return

        [2, 0, 0]
```

Now the all-nines case, `[9, 9]`:

```text
i = 1   9 -> 0      [9, 0]
i = 0   9 -> 0      [0, 0]
loop ends without returning
return [1] + digits   ->   [1, 0, 0]
```

## Why it works

A carry only matters as long as the digit receiving it overflows, and only 9 overflows. The first non-9 digit absorbs the carry completely, so the rest of the number is correct as it stands. If the loop finishes, every digit overflowed, the array is all zeros, and the missing carry becomes a new leading 1.

## Where it goes wrong

- Converting to an integer and back. It can work in Python, but the point is to handle the digits directly.
- Continuing the loop after a successful increment. Without the early `return`, you would keep adding to digits that should stay unchanged.
- Returning `digits` after the loop. For all nines that gives `[0, 0, 0]`, missing the leading 1.

## Cost

Time O(n) in the worst case (all nines), but usually only a digit or two is touched. Space O(1) extra, apart from the rare new array when every digit was a 9.
