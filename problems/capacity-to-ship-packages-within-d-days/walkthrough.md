## The idea

We must find the smallest ship capacity that gets every package delivered within `days`. Packages ship in order, one batch per day. Instead of searching over schedules, search over the answer itself.

The key property is monotonic: if a capacity works, any larger capacity also works, and if one fails, any smaller one fails. A yes/no answer that flips only once along a sorted range is exactly what binary search needs. So we binary search the capacity, and for each guess we check cheaply whether it is enough.

## Set-up

- `days_needed(cap)` answers "with capacity `cap`, how many days do we need?". It loads packages in order, and starts a new day when the next package would overflow.
- `lo = max(weights)`: the ship must at least carry the heaviest package.
- `hi = sum(weights)`: carrying everything in one day always works.

Invariant: the answer lies in `[lo, hi]`.

```text
weights = [1, 2, 3, 4, 5, 6]    days = 3

 capacity:   6 ......................... 21
             lo                         hi
```

## Step by step

```text
lo=6  hi=21  mid=13   days_needed(13) = 2 <= 3   works, hi = 13
lo=6  hi=13  mid=9    days_needed(9)  = 3 <= 3   works, hi = 9
lo=6  hi=9   mid=7    days_needed(7)  = 4 >  3   too small, lo = 8
lo=8  hi=9   mid=8    days_needed(8)  = 4 >  3   too small, lo = 9
lo=9  hi=9   stop     answer = 9
```

What does `days_needed(9)` do?

```text
day 1:  1 + 2 + 3 = 6     (adding 4 would make 10 > 9)
day 2:  4 + 5     = 9     (adding 6 would make 15 > 9)
day 3:  6
3 days
```

And `days_needed(8)`:

```text
day 1: 1+2+3 = 6    day 2: 4    day 3: 5    day 4: 6    -> 4 days, too many
```

## Why it works

Because feasibility flips once, when `days_needed(mid) <= days` the answer is `mid` or smaller, so `hi = mid` keeps it in range. When it fails, `mid` and everything below it are too small, so `lo = mid + 1`. The range shrinks until `lo == hi`, the smallest feasible capacity.

The greedy check is right because loading as many packages as fit each day never makes the schedule longer.

## Where it goes wrong

If `lo` started at 1 or 0, the check would try a capacity smaller than some package. In `days_needed`, that package would overflow even on an empty day, and the loop would count a new day without ever fitting it. The heaviest package as the lower bound rules this out.

The other trap is `hi = mid - 1`: the middle value might be the answer, so it must stay in range. Use `hi = mid` and `lo = mid + 1`.

## Cost

Time O(n log(sum)): about log of the range size guesses, each checked in O(n). Space O(1).
