def validate(result, case, scaffolds):
    strs = case["input"]["strs"]
    codec_class = case["entry"]
    encoded = codec_class().encode(list(strs))
    if not isinstance(encoded, str):
        return False, f"encode must return a str, got {type(encoded).__name__}"
    # decode on a fresh instance: no state may be shared between the two calls
    decoded = codec_class().decode(encoded)
    if decoded != case["expected"]:
        return False, f"round trip gave {decoded!r}, expected {case['expected']!r}"
    return True, ""
