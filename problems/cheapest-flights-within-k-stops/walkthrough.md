## The idea

Cheapest path sounds like Dijkstra, but there is a catch: the answer must use at most `k + 1` flights. The cheapest route overall may use too many flights, so a city's best price is not enough; you also need to know how many flights it took.

Bellman-Ford handles that naturally. Round `i` answers "what is the cheapest price to each city using at most `i` flights?" Run `k + 1` rounds and read off `dst`. No priority queue, no extra state.

## Set-up

- `cost[v]` is the cheapest known price to reach city `v`. Everything starts at `INF`, except `cost[src] = 0`.
- After round `i`, `cost[v]` is the cheapest price using at most `i` flights.
- `nxt` is a copy of `cost` taken at the start of each round. Updates go into `nxt`, but prices are read from `cost`.

```text
n = 4, src = 0, dst = 3, k = 1  (so 2 rounds)
flights: 0→1 (100)  1→2 (100)  2→0 (100)  1→3 (600)  2→3 (200)

city   0    1    2    3
cost   0   INF  INF  INF
```

## Step by step

```text
Round 1   (paths of at most 1 flight)
  0→1: cost[0]+100 = 100 < INF         nxt[1] = 100
  1→2: cost[1] is INF in the snapshot  no change
  1→3, 2→0, 2→3: sources are INF       no change

city   0    1    2    3
cost   0   100  INF  INF

Round 2   (paths of at most 2 flights)
  0→1: 0+100 = 100, not better
  1→2: 100+100 = 200 < INF             nxt[2] = 200
  1→3: 100+600 = 700 < INF             nxt[3] = 700
  2→3: cost[2] is INF in the snapshot  skipped this round

city   0    1    2    3
cost   0   100  200  700
```

`k + 1 = 2` rounds are done and `cost[3] = 700`. The route 0→1→2→3 costs 400 but needs three flights, so it is correctly not allowed.

## Why it works

By induction on the round number. Any route with at most `i` flights is a route with at most `i - 1` flights plus one last flight. Round `i` tries every last flight on top of the round `i - 1` prices, so it finds the best such route. Using the snapshot keeps "at most `i`" honest.

## Where it goes wrong

Relaxing in place, with no `nxt` copy, lets one round chain several flights. On the same data a single in-place pass in the listed order gives:

```text
in place, one pass:  cost = [0, 100, 200, 400]    <- 0→1→2→3, three flights in one round
snapshot, one round: cost = [0, 100, INF, INF]
```

The unreachable case: if `cost[dst]` is still `INF` after the rounds, return `-1`.

## Cost

Time O(k * E): `k + 1` rounds, each scanning every flight. Space O(n) for the two price arrays.
