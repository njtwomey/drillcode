## The idea

The obvious check is to simulate the drive: at each stop, add the people who board and remove the people who leave, and see if the car ever holds too many. Doing that by looping over every trip at every stop costs O(trips * stops).

There is a cheaper way to see it. Each trip only changes the load at two places: it goes up by `passengers` where the trip starts and goes down by the same amount where it ends. Record just those two changes in an array, then one running sum over the array gives the load at every stop.

## Set-up

- `last_stop` is the largest drop-off point. It sizes the array.
- `change` has one slot per stop. `change[x]` is the net number of people boarding at `x` (negative means net leaving).
- `load` is the running sum, which is the number of people in the car after stop `x` is handled.

Passengers get out at `to` before anyone gets in there. So a trip occupies the half-open range `[start, to)`: add at `start`, subtract at `to`.

## Step by step

Take `trips = [[2,1,5],[3,3,7]]` (passengers, start, to) with `capacity = 4`.

```text
stop      0   1   2   3   4   5   6   7
trip A        +2              -2
trip B                +3              -3
          ─────────────────────────────
change    0   2   0   3   0  -2   0  -3
```

Now sweep left to right, adding each slot to `load`:

```text
stop      0   1   2   3   4   5   6   7
change    0   2   0   3   0  -2   0  -3
load      0   2   2   5   5   3   3   0
                      ▲
                      load 5 > capacity 4  ──▶ return False
```

At stop 3 both trips are on board (2 + 3 = 5), which is over the limit, so the answer is `False`. With `capacity = 5` the sweep would finish and return `True`.

## Why it works

A running sum of the changes up to `x` is exactly "everyone who boarded at or before `x`, minus everyone who left at or before `x`". That is the car's load on the road leaving `x`. The load only changes at stops, so checking each stop checks every point on the route.

## Where it goes wrong

Subtracting at `to + 1`, or forgetting that `to` is already empty, breaks the hand-off case. With `[[3,2,7],[3,7,9]]` and capacity 3:

```text
stop     2   7   9
trip A  +3  -3
trip B      +3  -3
change  +3   0  -3      load stays 3, fine

if the drop-off were skipped at 7:   load at 7 would be 6, wrongly rejected
```

Also size the array to `last_stop + 1`, since `to` itself is an index. Trips can come in any order; the array does not care.

## Cost

Time O(n + m): one pass over the `n` trips, one pass over the `m` stops. Space O(m) for `change`.
