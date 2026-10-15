## The idea

Two questions need answering: "where and when did this customer get on?" and "what is the average for this route?". Both are lookups, so both become dictionaries.

For the average you do not need to remember every trip. You only need the total travel time and the number of trips for each route, because the average is `total / count`. Keeping those two numbers makes every call O(1).

## Set-up

- `self.open` maps a customer id to `(start station, check-in time)`. It holds only customers currently travelling. Invariant: an id is present exactly while that customer is checked in.
- `self.trips` maps `(start, end)` to `[total time, number of trips]`. The key is an ordered pair, so A to B and B to A are different routes.

```text
open  : {}
trips : {}
```

## Step by step

Use the usual example.

```text
checkIn(45, Leyton, 3)
checkIn(32, Paradise, 8)
checkIn(27, Leyton, 10)
  open  : {45: (Leyton, 3), 32: (Paradise, 8), 27: (Leyton, 10)}
  trips : {}

checkOut(45, Waterloo, 15)    pop 45 -> (Leyton, 3), took 15 - 3 = 12
  open  : {32: (Paradise, 8), 27: (Leyton, 10)}
  trips : {(Leyton, Waterloo): [12, 1]}

checkOut(27, Waterloo, 20)    pop 27 -> (Leyton, 10), took 10
  open  : {32: (Paradise, 8)}
  trips : {(Leyton, Waterloo): [22, 2]}

checkOut(32, Cambridge, 22)   pop 32 -> (Paradise, 8), took 14
  open  : {}
  trips : {(Leyton, Waterloo): [22, 2], (Paradise, Cambridge): [14, 1]}
```

Now `getAverageTime("Paradise", "Cambridge")` is 14 / 1 = 14.0 and `getAverageTime("Leyton", "Waterloo")` is 22 / 2 = 11.0. A later trip from Leyton at 24 to Waterloo at 38 takes 14, making the route `[36, 3]`, so the average becomes 12.0.

## Why it works

Every completed trip adds its duration and one to a single route entry, so `total / count` is always the mean of exactly the completed trips on that route. Popping the check-in at checkout means each journey is counted once and the id is free for the next one.

## Where it goes wrong

- Using `self.open[id]` and not removing it leaves stale data. A reused id would still work here because `checkIn` overwrites it, but `pop` keeps `open` small and honest.
- Keying routes by a sorted or unordered pair would merge A to B with B to A and give the wrong average.
- Integer division would lose the fraction. Use `/`, as the solution does, so 20 / 3 stays 6.666...

## Cost

All three calls are O(1). Space is O(open check-ins + distinct routes), not the number of trips, because only totals are stored.
