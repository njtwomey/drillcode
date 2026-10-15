## The idea

You can buy and sell as many times as you like, but after a sale you must wait one day before buying again. Instead of searching over trade schedules, describe where you can be at the end of each day and what profit that state has earned. This is a small state machine, and each day we update every state from yesterday's states.

There are three states:

- `held`: you own a share.
- `sold`: you just sold today, so tomorrow is a forced cooldown.
- `rest`: you own nothing and are free to buy tomorrow.

## Set-up

- `held = -inf`: before day 0 holding a share is impossible. `-inf` stops that state ever being chosen until a real buy happens.
- `sold = -inf`: likewise impossible.
- `rest = 0`: nothing owned, no profit yet.

Each state stores the best profit achievable while in that state at the end of the day.

```text
                 buy
        rest ----------> held
         ^  ^              |
   wait  |  | cooldown     | sell
         |  +-- sold <-----+
         +---(stay)
```

Transitions: `held` = stay held, or buy from `rest` (never from `sold`, which is the cooldown). `sold` = sell yesterday's `held`. `rest` = stay resting, or arrive from yesterday's `sold`.

## Step by step

`prices = [1, 2, 3, 0, 2]`. Each day, in this order: `sold = held + price`, then `held = max(held, rest - price)`, then `rest = max(rest, prev_sold)`, where `prev_sold` is the old `sold`.

```text
price     held    sold    rest
start     -inf    -inf      0
  1        -1     -inf      0     buy at 1: held = 0 - 1
  2        -1       1       0     sell: sold = -1 + 2
  3        -1       2       1     sell instead at 3: sold = -1 + 3;
                                  rest = max(0, old sold 1)
  0         1      -1       2     buy at 0 from rest: held = 1 - 0;
                                  rest = max(1, old sold 2)
  2         1       3       2     sell: sold = 1 + 2
```

Notice the price-0 row. `held` is built from `rest` (1), the profit banked before the cooldown ended, not from `sold` (2), because buying the day after a sale is not allowed. The `sold = -1` there is just the poor option of selling at 0.

The final answer is `max(sold, rest, 0) = max(3, 2, 0) = 3`: buy at 1, sell at 3, cool down, buy at 0, sell at 2.

## Why it works

Every legal schedule is a path through the three states, and each day's transition covers exactly the moves allowed from the previous day. Because `held` can only be reached from `rest`, never from `sold`, the cooldown is enforced by the structure itself. Ending while holding is never better than having sold, so it is excluded from the answer.

## Where it goes wrong

The update order matters. `sold` reads yesterday's `held`, `held` reads yesterday's `rest`, and `rest` reads yesterday's `sold`, so `prev_sold` is saved first and `rest` is updated last. Updating `held` before `sold` would sell a share bought the same day.

```text
wrong:  held = max(held, rest - price)   # buys today
        sold = held + price               # sells it the same day
```

## Cost

Time O(n): one pass. Space O(1): three numbers (plus `prev_sold`), however many days.
