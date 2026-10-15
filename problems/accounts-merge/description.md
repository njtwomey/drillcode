`accounts[i]` is a list whose first entry is a person's name and whose remaining entries are email addresses belonging to that account. Two accounts belong to the same person if they share at least one email. Different people may have the same name, so a shared name alone proves nothing.

Merge the accounts. Each result is the name followed by that person's distinct emails in sorted order. The results may be returned in any order.

Constraints:
- `1 <= len(accounts) <= 1000`
- `2 <= len(accounts[i]) <= 10`
- Names and emails are at most 30 characters.
