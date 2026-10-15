## The idea

Bursting a balloon scores its value times its two current neighbours. The trouble with thinking forwards ("which balloon do I burst first?") is that every burst changes who the neighbours are, so the remaining pieces depend on each other.

Flip the question: which balloon in a range is burst LAST? When `k` is the last one left between two fixed balloons `l` and `r`, its neighbours at that moment are exactly `l` and `r`, whatever happened before. And everything popped on its left and everything popped on its right can no longer interact, because `k` is still standing between them. The problem splits into two independent smaller ones.

## Set-up

- `vals` is `nums` with a `1` added at both ends. A balloon on the edge is multiplied by an imaginary 1. An empty input becomes `[1, 1]` and scores 0.
- `dp[l][r]` is the most coins from bursting every balloon strictly between positions `l` and `r`, with `l` and `r` themselves left in place.
- `dp[l][l+1]` is 0: nothing lies between neighbours. That is the default zero from the table.
- The answer is `dp[0][size - 1]`: everything between the two sentinels.

For `nums = [3, 1, 5]`:

```text
index:   0  1  2  3  4
vals:  [ 1, 3, 1, 5, 1 ]
         ^              ^
       sentinel      sentinel
```

## Step by step

Intervals are processed by increasing `gap = r - l`, because `dp[l][r]` reads `dp[l][k]` and `dp[k][r]`, which are shorter. For each interval try every `k` strictly between and keep the best `vals[l] * vals[k] * vals[r] + dp[l][k] + dp[k][r]`.

```text
gap 2  (one balloon between)
  dp[0][2]: k=1  1*3*1 = 3                         -> 3
  dp[1][3]: k=2  3*1*5 = 15                        -> 15
  dp[2][4]: k=3  1*5*1 = 5                         -> 5

gap 3  (two balloons between)
  dp[0][3]: k=1  1*3*5 + dp[0][1] + dp[1][3] = 15+0+15 = 30
            k=2  1*1*5 + dp[0][2] + dp[2][3] = 5+3+0   = 8     -> 30
  dp[1][4]: k=2  3*1*1 + dp[1][2] + dp[2][4] = 3+0+5   = 8
            k=3  3*5*1 + dp[1][3] + dp[3][4] = 15+15+0 = 30    -> 30

gap 4  (all three)
  dp[0][4]: k=1  1*3*1 + dp[0][1] + dp[1][4] = 3+0+30  = 33
            k=2  1*1*1 + dp[0][2] + dp[2][4] = 1+3+5   = 9
            k=3  1*5*1 + dp[0][3] + dp[3][4] = 5+30+0  = 35    -> 35
```

The table after filling (upper triangle):

```text
          r=0  r=1  r=2  r=3  r=4
   l=0     .    0    3   30   35
   l=1          .    0   15   30
   l=2               .    0    5
   l=3                    .    0
```

The answer is 35. The winning choice was `k=3`: burst the `5` last, after `3` and `1` had earned 30 between the sentinel and the `5`.

## Why it works

Whichever balloon `k` goes last in `(l, r)`, the score from the last burst is fixed at `vals[l] * vals[k] * vals[r]`. The other balloons in `(l, k)` are burst while `l` and `k` still stand, and those in `(k, r)` while `k` and `r` stand. Neither side can see the other, so the best total is the sum of the two sub-answers. Trying every `k` covers every possible last balloon.

## Where it goes wrong

- Choosing the first balloon to burst. The neighbours of the leftover pieces then depend on this choice and the pieces are not independent.
- Skipping the padding. Edge balloons would need special cases.
- Iterating `l` and `r` in the wrong order, so `dp[l][k]` or `dp[k][r]` is still 0 when read. Ordering by gap prevents this.
- Dropping zero-valued balloons from the input to save work. Their own bursts score nothing, but as neighbours they still affect what others score, so they must stay in `vals`.

## Cost

Time O(n³): O(n²) intervals, up to n choices of `k` each. Space O(n²) for the table.
