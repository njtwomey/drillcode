def validate(result, case, scaffolds):
    n = case["args"]["numCourses"]
    prerequisites = case["args"]["prerequisites"]
    if case["expected"] == []:
        return (result == [], f"expected [] for an impossible schedule, got {result}")
    if not isinstance(result, list) or sorted(result) != list(range(n)):
        return False, f"result must contain each of 0..{n - 1} exactly once, got {result}"
    position = {course: i for i, course in enumerate(result)}
    for course, pre in prerequisites:
        if position[pre] > position[course]:
            return False, f"course {course} comes before its prerequisite {pre}"
    return True, ""
