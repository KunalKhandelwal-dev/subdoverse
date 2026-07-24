from subdoverse.utils.helpers import normalize_hostname

def merge_results(sources):
    """
    Merge multiple enumeration result lists
    while preserving discovery order
    and removing duplicates.
    """

    merged = []

    seen = set()

    for source in sources:

        for host in source:

            host = normalize_hostname(host)

            if not host:
                continue

            if host in seen:
                continue

            seen.add(host)

            merged.append(host)

    return merged