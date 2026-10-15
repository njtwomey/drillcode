"""uv run python scripts/verify_links.py -- check every slug/number/premium flag against LeetCode's GraphQL API.

(Plain HEAD requests get a 403 from LeetCode's bot protection even for non-existent pages.)
"""

import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from _common import load_index

QUERY = "query q($s:String!){question(titleSlug:$s){questionFrontendId title isPaidOnly}}"


def check(entry):
    body = json.dumps({"query": QUERY, "variables": {"s": entry["slug"]}}).encode()
    request = urllib.request.Request(
        "https://leetcode.com/graphql", body,
        {"Content-Type": "application/json", "Referer": "https://leetcode.com", "User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            question = json.load(response)["data"]["question"]
    except Exception as e:
        return f"{entry['slug']}: request failed ({e})"
    if question is None:
        return f"{entry['slug']}: no such problem on LeetCode"
    problems = []
    if int(question["questionFrontendId"]) != entry["number"]:
        problems.append(f"number is {question['questionFrontendId']}, index says {entry['number']}")
    if question["isPaidOnly"] != entry["premium"]:
        problems.append(f"premium is {question['isPaidOnly']}, index says {entry['premium']}")
    return f"{entry['slug']}: " + "; ".join(problems) if problems else None


def main():
    index = load_index()
    with ThreadPoolExecutor(8) as pool:
        errors = [e for e in pool.map(check, index) if e]
    print("\n".join(errors) or f"all {len(index)} links verified")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
