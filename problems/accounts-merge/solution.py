"""Accounts Merge (#721, medium)

Approach: Union-find keyed by email, joining every email of an account to its first,
    then group emails by root and sort.
Tricks: Union emails rather than accounts and look the name up from the root, because
    equal names do not imply the same person.
Edge cases:
  - Same name, no shared email
  - Transitive merge across three accounts
  - Repeated email within one account

Time O(N log N * α(N)) for N emails, space O(N).
"""

from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        # Union-find over emails, not accounts: an email is the real identity, and
        # two accounts belong to one person exactly when they are linked by emails.
        parent = {}
        owner = {}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for name, *emails in accounts:
            for email in emails:
                if email not in parent:
                    parent[email] = email
                    owner[email] = name
                # Tie every email of this account to the account's first one.
                parent[find(email)] = find(emails[0])
        # Names can repeat across different people, so group by root email and only
        # then look the name up.
        groups = defaultdict(list)
        for email in parent:
            groups[find(email)].append(email)
        return [[owner[root]] + sorted(emails) for root, emails in groups.items()]
