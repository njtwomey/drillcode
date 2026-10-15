## The idea

Cars drive toward a target on a single-lane road. A car cannot pass the one ahead; if it catches up, it slows to that car's speed and they travel together as a fleet. We count the fleets that arrive.

The question for each car is: would it reach the target no later than whoever is ahead? If so, it will be caught behind them (or reach the end at the same moment) and belongs to their fleet. If it would take longer even when unobstructed, nobody ahead can hold it back, so it forms a new fleet.

That makes arrival time the useful number, and the right order to look at cars is from the one nearest the target backward.

## Set-up

- `cars = sorted(zip(position, speed), reverse=True)` lists cars from nearest the target to farthest.
- `slowest` is the arrival time of the nearest fleet ahead. It starts at `0.0`.
- `fleets` counts them.
- `time = (target - pos) / spd` is a car's arrival time if it were alone.

Invariant: `slowest` is the arrival time of the fleet at the front of what we have processed so far.

```text
target = 12
position = [10, 8, 0, 5, 3]    speed = [2, 4, 1, 1, 3]

sorted by position, nearest first:
 pos:    10    8    5    3    0
 speed:   2    4    1    3    1
```

## Step by step

```text
pos 10, speed 2:  time = (12-10)/2 = 1.0   > slowest 0.0
                  new fleet.  fleets = 1,  slowest = 1.0

pos  8, speed 4:  time = (12-8)/4  = 1.0   not > 1.0
                  ties: reaches the target with the front fleet, merges
                  fleets = 1

pos  5, speed 1:  time = (12-5)/1  = 7.0   > 1.0
                  too slow to catch the fleet ahead, a new fleet
                  fleets = 2,  slowest = 7.0

pos  3, speed 3:  time = (12-3)/3  = 3.0   not > 7.0
                  would catch the slow car at 5, joins it
                  fleets = 2

pos  0, speed 1:  time = (12-0)/1  = 12.0  > 7.0
                  never catches up, new fleet
                  fleets = 3,  slowest = 12.0
```

The answer is `3`: the fleet of cars at 10 and 8, the fleet of cars at 5 and 3, and the lone car at 0.

## Why it works

Cars cannot pass, so the arrival time of a fleet is the arrival time of its front car. A car behind has an unobstructed time; its real time is the larger of that and the time of the fleet in front. A new fleet starts exactly when the unobstructed time is larger than the fleet ahead, which is what `time > slowest` tests. Merged cars never raise `slowest`, since their own time is no larger.

## Where it goes wrong

- Using `>=` would count a tie as a new fleet. Two cars reaching the target at the same moment are in one fleet, so only strictly larger times count.
- Skipping the sort fails, since the input positions are not ordered.
- Integer division instead of `/` would truncate arrival times and mis-compare close ones.

## Cost

Time O(n log n) for the sort; the pass is O(n). Space O(n) for the sorted list of pairs.
