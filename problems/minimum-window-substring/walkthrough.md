## The idea

Checking every substring of `s` against `t` is far too slow. Instead, slide a window with two pointers. Move `right` forward until the window holds everything `t` needs. Then move `left` forward to squeeze out anything unnecessary, and note the length. Both pointers only ever move forward, so the work is linear.

The awkward part is knowing, in O(1), whether the window is valid. The solution does that with one counter instead of comparing two dictionaries.

## Set-up

- `need[ch]` starts as how many copies of `ch` `t` asks for. As the window grows it is decremented. A positive value means the window still lacks that many; zero or negative means it has enough, with a surplus.
- `missing` starts at `len(t)` and counts required characters still lacking. The window is valid exactly when `missing == 0`.
- `left` is the start of the window; `right` is the loop variable.
- `best_start`, `best_len` remember the best window so far.

```text
index:  0 1 2 3 4 5 6 7 8 9 10 11 12
s    :  A D O B E C O D E B A  N  C        t = "ABC"
        ^
        left = right = 0

need = {A:1, B:1, C:1}   missing = 3
```

## Step by step

For each `right`: if `need[ch] > 0` the character helps, so `missing` drops. Then `need[ch]` is always decremented (it goes negative for extras and for letters not in `t`). When `missing == 0`, shrink `left` while `need[s[left]] < 0`, record the window, then deliberately drop `s[left]` (a needed letter) to break validity and keep searching.

```text
right=0  A  missing 3 -> 2
right=3  B  missing 2 -> 1
right=5  C  missing 1 -> 0   window "ADOBEC" (left=0), valid
            s[left]=A has need 0, not surplus: no shrink. Record len 6.
            Drop A: need[A]=1, missing=1, left=1.

right=10 A  missing 1 -> 0, valid
            shrink from left=1 past D, O, B, E (all surplus):
            left=5, window "CODEBA", len 6, ties the best.
            Drop C: need[C]=1, missing=1, left=6.

right=12 C  missing 1 -> 0, valid
            shrink from left=6 past O, D, E: left=9, window "BANC",
            len 4, new best.
```

```text
 A D O B E C O D E B A N C
                   ^-----^   answer "BANC"
                   left  right
```

## Why it works

When `missing == 0` after shrinking, `[left, right]` is the shortest valid window ending at `right`, because the shrink loop only removes characters that are surplus. Every possible end is visited. Dropping a needed character afterwards just restarts the search for the next valid end, without losing any candidate.

## Where it goes wrong

- Only counting a character as progress when `need[ch] > 0`. If you decrement `missing` on every match, a second `A` when `t` wants one would wrongly count.
- The final `inf` check is what turns "never valid" into `""`; without it the slice is garbage.
- Shrinking with `<= 0` instead of `< 0` would remove a needed letter and make the recorded window invalid.

## Cost

Time O(m + n): `left` and `right` each move at most `m` steps, and the inner loop adds nothing beyond that. Space O(alphabet) for `need`.
