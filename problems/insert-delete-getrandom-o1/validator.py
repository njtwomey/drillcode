import random


def validate(result, case, scaffolds):
    ops = case["args"]["ops"]
    obj = case["entry"]()
    model = set()
    random.seed(0)
    for step, (name, args) in enumerate(ops):
        if name == "insert":
            expected = args[0] not in model
            model.add(args[0])
            actual = obj.insert(args[0])
        elif name == "remove":
            expected = args[0] in model
            model.discard(args[0])
            actual = obj.remove(args[0])
        else:
            actual = obj.getRandom()
            if actual not in model:
                return False, f"step {step}: getRandom returned {actual}, not in {sorted(model)}"
            continue
        if actual is not expected:
            return False, f"step {step}: {name}({args[0]}) returned {actual}, expected {expected}"
    if model:
        seen = {obj.getRandom() for _ in range(200)}
        if not seen <= model:
            return False, f"getRandom returned {sorted(seen - model)}, not in the set"
        if len(model) <= 10 and seen != model:
            return False, f"200 calls never returned {sorted(model - seen)}; getRandom looks biased"
    return True, ""
