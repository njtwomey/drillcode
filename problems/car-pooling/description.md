A car with `capacity` empty seats drives in one direction past stops numbered by distance from the start. Each entry `trips[i] = [numPassengers, from, to]` is a group that boards at stop `from` and gets off at stop `to`. The car never turns around, and trips are not sorted.

Return `True` if every trip can be completed without ever carrying more than `capacity` passengers, else `False`. A group leaving at a stop frees its seats for groups boarding at that same stop.

Constraints:
- `1 <= len(trips) <= 1000`
- `1 <= numPassengers <= 100`
- `0 <= from < to <= 1000`
- `1 <= capacity <= 10^5`
