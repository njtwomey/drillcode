## The idea

A string like `3[a2[c]]` has brackets inside brackets. Each `]` closes the most recent unclosed `[`, which is stack behaviour. So scan once, and every time a group opens, park the unfinished outer work on a stack and start a clean slate for the inside. When the group closes, pop the outer work and glue the repeated inside text onto it.

## Set-up

- `curr` is the text built so far at the current nesting level.
- `num` is the repeat count being read for the group that is about to open. Digits arrive one at a time, so `num = num * 10 + int(ch)` handles counts like `12`.
- `stack` holds `(text, count)` pairs for the outer levels waiting to be resumed.

The three symbols mean:

- A digit extends `num`.
- `[` saves `(curr, num)` and resets both.
- `]` pops `(prev, count)` and sets `curr = prev + curr * count`.
- Any other character is a letter and goes onto `curr`.

## Step by step

Decode `3[a2[c]]`. Each row shows the state after that character:

```text
char   curr    num   stack
 3     ""      3     []
 [     ""      0     [("", 3)]
 a     "a"     0     [("", 3)]
 2     "a"     2     [("", 3)]
 [     ""      0     [("", 3), ("a", 2)]
 c     "c"     0     [("", 3), ("a", 2)]
 ]     "acc"   0     [("", 3)]          pop ("a",2): "a" + "c"*2
 ]     "accaccacc" 0 []                 pop ("",3):  "" + "acc"*3
```

The answer is `curr = "accaccacc"`. The stack gets as deep as the nesting:

```text
after the second [ :     ┌──────────┐
                         │ ("a", 2) │   top: resume this first
                         │ ("", 3)  │
                         └──────────┘
```

## Why it works

At any moment `curr` is the finished text of the innermost open group so far, and the stack holds the text and repeat count of each enclosing group. Closing a group completes exactly one level, and the result slots in as part of the next level out. Nothing is expanded until its brackets close, so the order is always inside out.

## Where it goes wrong

Forgetting to reset `curr` and `num` on `[`. Then the inside text starts with the outer letters, and the next count is added to the old one:

```text
"a2[b]"   correct: "a" + "b"*2 = "abb"

if "[" did not reset curr:
  at "[" push ("a", 2), but curr stays "a"
  b      curr "ab"
  "]"    curr = "a" + "ab"*2 = "aabab"   wrong
```

Reading only one digit also breaks `10[a]` (it would see 1, then 0). The multi-digit formula covers this.

## Cost

Time and space O(L), where L is the length of the decoded output: each repeat copies text, and the stack holds at most the current partial strings.
