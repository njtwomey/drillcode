## The idea

Reversing digits is a loop of two moves: peel the last digit off the input (`x % 10`, `x // 10`) and append it to the result (`result * 10 + digit`). The hard part is the 32-bit limit. The reversed number of a valid input can be too big, and the problem says you cannot lean on a wider type to notice afterwards.

So we check before each append whether `result * 10 + digit` would pass the limit, and give up with `0` if so. Python integers never overflow, but this mimics what a fixed-width language must do.

## Set-up

- `sign` remembers whether `x` was negative, and we work on `abs(x)`. Python's `//` and `%` floor towards negative infinity, so peeling digits from a negative number would misbehave.
- `limit` is the largest magnitude allowed: `2**31 - 1` for positives but `2**31` for negatives, because the 32-bit range is `[-2**31, 2**31 - 1]`.
- `result` is the reversed number built so far, starting at 0.

```text
x = 123   sign = +1   limit = 2147483647   result = 0
```

## Step by step

`divmod(x, 10)` gives the remaining number and the last digit together.

```text
x     digit   result before   result after
123    3          0                3
12     2          3               32
1      1         32              321
0   (loop ends)   return sign * result = 321
```

A negative input with trailing zeros, `-120`, becomes `x = 120`: digits 0, 2, 1 give results 0, 2, 21, so the answer is `-21`. The leading zero of the reversed number simply vanishes.

Now an overflow, `x = 1534236469`. The check `result > (limit - digit) // 10` is the same as asking whether `result * 10 + digit > limit`.

```text
digit    result   bound=(limit-digit)//10   result > bound?
  9             0   214748363                no
  6             9   214748364                no
  4            96   214748364                no
  ...
  3       9646324   214748364                no
  1     964632435   214748364                YES -> return 0
```

The 10th append would make 9646324351, far past 2147483647.

## Why it works

`result * 10 + digit > limit` rearranges to `result * 10 > limit - digit`, and with integers that is `result > (limit - digit) // 10`. So the check fires exactly when the append would overflow, and never earlier or later. Once the loop finishes, every append was in range.

## Where it goes wrong

Getting the bound wrong. The 32-bit range is asymmetric, and `limit` follows it: `2**31` for negatives, `2**31 - 1` for positives. The check must also happen before the append, not after, since a fixed-width integer would already have wrapped.

Peeling digits straight from a negative number is the other trap: `-123 // 10` is `-13`, not `-12`.

```text
-123 // 10  -> -13      (floors away from zero)
 123 // 10  ->  12
```

## Cost

Time O(log x): one iteration per decimal digit. Space O(1): a few integers.
