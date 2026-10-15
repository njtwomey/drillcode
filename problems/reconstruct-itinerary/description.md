You are given `tickets`, a list of `[from, to]` airport-code pairs, each one a flight. Build an itinerary that starts at `"JFK"` and uses every ticket exactly once, returning the airports visited in order.

If several itineraries exist, return the one that is smallest when compared as a sequence of airport names in lexical order. A valid itinerary is guaranteed to exist. Tickets may repeat, and the same pair of airports can have several flights between them.

Constraints:
- `1 <= len(tickets) <= 300`
- Airport codes are 3 uppercase letters
- Greedily taking the smallest next airport can get stuck
