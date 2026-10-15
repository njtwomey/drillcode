"""uv run python scripts/run_tests.py [slug ...]  -- run reference solutions against tests.yaml."""

import signal
import sys

from _common import PROBLEMS, load_spec, problem_dirs, read_optional

import runner

LIMIT_SECONDS = 5


def _on_alarm(signum, frame):
    raise runner.CaseTimeout()


def main():
    slugs = sys.argv[1:] or problem_dirs()
    signal.signal(signal.SIGALRM, _on_alarm)
    failed_problems = []
    for slug in slugs:
        directory = PROBLEMS / slug
        if not directory.is_dir():
            print(f"{slug}: no such problem directory")
            failed_problems.append(slug)
            continue
        spec = load_spec(slug)
        source = (directory / "solution.py").read_text()
        validator = read_optional(directory / "validator.py")
        passed = 0
        for case in spec["cases"]:
            signal.alarm(LIMIT_SECONDS)
            try:
                result = runner.run_case(source, spec, case, validator)
            except runner.CaseTimeout:
                result = {"name": case["name"], "status": "timeout", "ms": LIMIT_SECONDS * 1000,
                          "message": "Time limit exceeded", "expected": None, "actual": None}
            finally:
                signal.alarm(0)
            if result["status"] == "pass":
                passed += 1
            print(f"  {result['status'].upper():7} {slug} :: {result['name']} ({result['ms']:.2f} ms)")
            if result["status"] != "pass":
                print(f"          expected: {result['expected']!r}")
                print(f"          actual:   {result['actual']!r}")
                if result["message"]:
                    print("          " + result["message"].strip().replace("\n", "\n          "))
        total = len(spec["cases"])
        print(f"{slug}: {passed}/{total} passed")
        if passed != total:
            failed_problems.append(slug)
    print(f"\n{len(slugs) - len(failed_problems)}/{len(slugs)} problems green")
    if failed_problems:
        print("FAILED: " + ", ".join(failed_problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
