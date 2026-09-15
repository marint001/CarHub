def find_lowest_available_code(existing_codes, prefix):
    """Return the lowest never-used internal code for a prefix.

    Examples:
        existing_codes = ["0020001", "0020002", "0020004"]
        prefix = "002"
        result = "0020003"

    Rules:
        - Ignore codes belonging to another prefix.
        - Ignore malformed codes whose suffix is not numeric.
        - The numeric suffix starts at 1.
        - Pad the suffix to at least four digits.

    This function deliberately has no database access. Keeping the algorithm
    independent makes it easy to understand and test before Django integration.
    """
    used_numbers = set()

    for code in existing_codes:
        if not code.startswith(prefix):
            continue

        suffix = code[len(prefix):]

        if suffix.isdigit():
            used_numbers.add(int(suffix))

    candidate = 1
    while candidate in used_numbers:
        candidate += 1

    return f"{prefix}{candidate:04d}"

def assign_code(model_class, prefix, code_field='code'):
    existing_codes = model_class.objects.values_list(code_field, flat=True)
    return find_lowest_available_code(list(existing_codes), prefix)
