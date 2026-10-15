## The idea

You want the biggest `price[sell] - price[buy]` with the buy day before the sell day. Trying every pair is O(n^2). But for any chosen sell day, the best buy day is simply the cheapest day before it. So walk the days once, remember the cheapest price seen so far, and ask on each day: "if I sold today, how much would I make?"

## Set-up

- `lowest` is the cheapest price seen so far. It starts at infinity so the first price replaces it.
- `best` is the largest profit found so far. It starts at 0, which is also the answer when no profitable trade exists.

Invariant: at the end of each day, `lowest` is the minimum of all prices up to and including that day, and `best` is the best profit using only those days.

```text
prices:  7   1   5   3   6   4
index:   0   1   2   3   4   5
         ^
      lowest = inf, best = 0
```

## Step by step

For each `price`, first update `lowest`, then update `best` with `price - lowest`.

```text
day  price  lowest  price-lowest  best
 0     7      7          0          0
 1     1      1          0          0     new cheapest
 2     5      1          4          4
 3     3      1          2          4
 4     6      1          5          5     buy at 1, sell at 6
 5     4      1          3          5
```

The answer is 5.

## Why it works

The best trade sells on some day `j`. For that `j` the best buy is the minimum of the earlier prices, which is what `lowest` holds when the loop reaches `j`. Taking the maximum over all `j` therefore covers every candidate that could be optimal. Since `lowest` only ever uses days up to the current one, the buy never comes after the sell.

## Where it goes wrong

Update `lowest` before computing the profit. Then on a new cheapest day the profit is `price - price = 0`, not a negative number. If you reversed the order the code would still be right here, since `best` starts at 0, but updating first makes the same-day case obviously harmless.

A strictly falling list shows why `best` starts at 0 and not at the first difference:

```text
prices: 5 4 3 2 1
price-lowest each day: 0 0 0 0 0   -> best stays 0 (do not trade)
```

## Cost

Time O(n), a single pass. Space O(1), two numbers.
