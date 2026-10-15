## The idea

An address is four pieces, each 1 to 3 digits. That gives at most 3 choices per piece, so at most 3^4 ways to cut the string, a tiny search. Backtracking explores it: choose the first piece, then the second from what remains, and so on, keeping only cuts where every piece is legal and the digits run out exactly on the fourth piece.

## Set-up

- `path` is the list of pieces chosen so far, shared and mutated.
- `start` is the index in `s` where the next piece begins.
- `parts_left` is `4 - len(path)`.
- A piece is legal when it is at most 255 and has no leading zero (the single digit `"0"` is fine).

Two cheap checks cut the search:

- If the remaining digits do not fit in the remaining pieces (`parts_left <= remaining <= 3 * parts_left` fails), stop that branch.
- While trying lengths 1, 2, 3, `break` at the first illegal piece, because a longer piece with the same start is only bigger, or still has the leading zero.

```text
s = "25525"       path = []      start = 0      parts_left = 4
```

## Step by step

The tree of choices, indented by depth. Each line shows `path` after the choice.

```text
['2']
  ['2','5']
    ['2','5','5']
      ['2','5','5','2']    four pieces, start=4, one digit left -> rejected
      ['2','5','5','25']   uses all digits -> 2.5.5.25
    ['2','5','52']
      ['2','5','52','5']   -> 2.5.52.5
    (piece "525" > 255: break)
  ['2','55']
    ['2','55','2']
      ['2','55','2','5']   -> 2.55.2.5
    (['2','55','25']: no digits left for the last piece, pruned)
  (piece "552" > 255: break)
['25']
  ['25','5']
    ['25','5','2']
      ['25','5','2','5']   -> 25.5.2.5
    (['25','5','25']: pruned too)
  (['25','52']: 1 digit left for 2 pieces, pruned)
  (piece "525" > 255: break)
(['255']: 2 digits left for 3 pieces, pruned)
```

Answers: `2.5.5.25`, `2.5.52.5`, `2.55.2.5`, `25.5.2.5`.

## Why it works

Every valid address is one particular sequence of piece lengths, and the loop tries all lengths 1 to 3 at each of the four levels, so each is reachable. Only legal pieces enter `path`, and a four-piece path counts only if `start == len(s)`, so no digit is dropped or added. The `break` is safe because validity can only get worse as the piece grows.

## Where it goes wrong

- Rejecting `"0"` itself. Only a longer piece starting with 0 is bad (the length check handles this).
- Using `continue` instead of `break` for an illegal piece. It still gives the right answer here but does needless work.
- Accepting four pieces without checking that all digits were used: `"25525"` could give `2.5.5.2` and drop a digit.

## Cost

The depth is fixed at 4 and the fan-out is at most 3, so the search is bounded by a constant: time O(1), space O(1) apart from the output.
