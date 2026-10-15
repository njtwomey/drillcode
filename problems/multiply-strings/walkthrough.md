## The idea

You already know how to multiply by hand: multiply digit by digit, line the partial products up by place value, add the columns and carry. The only trick is doing it without turning the whole strings into integers.

The useful fact is where each digit product lands. An `m`-digit number times an `n`-digit number has at most `m + n` digits, so we allocate that many columns up front. Digit `i` of `num1` times digit `j` of `num2` belongs in column `i + j + 1`, with its carry going to column `i + j`. Columns are numbered from the left, like the strings.

## Set-up

- If either input is `"0"` we return `"0"` immediately, which also guarantees the product has no all-zero digits to worry about.
- `result` is a list of `m + n` zeros, one per column. After processing, every entry is a single digit.
- We loop `i` and `j` from the right, the way you multiply on paper, and add into whatever the column already holds.

```text
num1 = "23"   num2 = "45"     expected 23 * 45 = 1035

column:   0  1  2  3
result: [ 0, 0, 0, 0 ]
```

## Step by step

Each step computes `total = digit * digit + result[i + j + 1]`, keeps `total % 10` in that column and adds `total // 10` to the column on its left.

```text
i  j   digits   total          result after
1  1   3 * 5    15 + 0  = 15   [0, 0, 1, 5]
1  0   3 * 4    12 + 1  = 13   [0, 1, 3, 5]
0  1   2 * 5    10 + 3  = 13   [0, 2, 3, 5]
0  0   2 * 4     8 + 2  = 10   [1, 0, 3, 5]
```

Look at the third row: `i=0, j=1` writes to column `i + j + 1 = 2`, which already held 3 from the row before, so the total is `10 + 3`. The columns end as `1035`, and `23 * 45 = 1035`.

## Why it works

Digit `i` of `num1` has place value `10^(m-1-i)` and digit `j` of `num2` has `10^(n-1-j)`. Their product has place value `10^(m+n-2-i-j)`, which is exactly the units column at index `i + j + 1` (the tens are one column left, at `i + j`). Adding into the column's current value before splitting means carries are folded in as we go. The running column value stays small enough that one `// 10` and `% 10` split is always sufficient.

## Where it goes wrong

Leading zeros. The product has `m + n` or `m + n - 1` digits, so `result[0]` may stay 0. We drop at most one.

```text
"99" * "9"   -> result = [8, 9, 1]    891, three digits (m+n = 3)
"2"  * "3"  -> result = [0, 6]       strip the 0 -> "6"
```

Writing the digit product into the column with `=` instead of adding to what is there would overwrite earlier partial products.

## Cost

Time O(m * n): one multiplication per pair of digits. Space O(m + n) for the `result` list.
