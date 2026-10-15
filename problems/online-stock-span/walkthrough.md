## The idea

The span of today's price is how many consecutive days, ending today, had a price at most today's. Scanning backwards every call costs O(n). The trick is to notice that once a later day has a higher price, the earlier days it covers never need looking at one by one again. Keep a stack where each entry stands for a whole run of days, and let a new price swallow every entry it beats.

## Set-up

- `self.stack` holds `(price, span)` pairs. Prices on the stack are strictly decreasing from bottom to top. Each entry means "this price, plus the `span - 1` days immediately before it, were all at most this price".
- `span = 1` in `next`: today always counts.

```text
(bottom)                       (top)
stack = []
```

## Step by step

For each price, pop while the top's price is at most `price`, add each popped span to `span`, then push `(price, span)`. Using prices 100, 80, 60, 70, 60, 75, 85:

```text
next(100)  nothing to pop              push (100,1)     -> 1
           stack: [(100,1)]

next(80)   100 <= 80? no               push (80,1)      -> 1
           stack: [(100,1) (80,1)]

next(60)   80 <= 60? no                push (60,1)      -> 1
           stack: [(100,1) (80,1) (60,1)]

next(70)   60 <= 70: pop, span=2
           80 <= 70? no                push (70,2)      -> 2
           stack: [(100,1) (80,1) (70,2)]

next(60)   70 <= 60? no                push (60,1)      -> 1
           stack: [(100,1) (80,1) (70,2) (60,1)]

next(75)   60 <= 75: pop, span=2
           70 <= 75: pop, span=4
           80 <= 75? no                push (75,4)      -> 4
           stack: [(100,1) (80,1) (75,4)]

next(85)   75 <= 85: pop, span=5
           80 <= 85: pop, span=6
           100 <= 85? no               push (85,6)      -> 6
           stack: [(100,1) (85,6)]
```

The results are `1, 1, 1, 2, 1, 4, 6`.

## Why it works

An entry on the stack is the nearest earlier day with a price greater than any of the days its span covers. When a new price pops an entry, every day that entry covered is also at most the new price, so they can be added in one step by adding the stored span. The first entry that is not popped is the first day higher than today, which is exactly where the span ends.

## Where it goes wrong

- Popping on `<` instead of `<=`. Equal prices count toward the span, so with three 5s the answers are 1, 2, 3, not 1, 1, 1.
- Storing only prices and re-walking history. That works but loses the O(1) amortised cost.
- Forgetting to add the popped span and adding just `1` per pop undercounts days that were already merged.

```text
prices 5, 5, 5
  next(5): push (5,1)                     -> 1
  next(5): pop (5,1), span 2, push (5,2)  -> 2
  next(5): pop (5,2), span 3, push (5,3)  -> 3
```

## Cost

Time O(1) amortised per call: each price is pushed once and popped at most once. Space O(n) for the stack in the worst case (strictly decreasing prices).
