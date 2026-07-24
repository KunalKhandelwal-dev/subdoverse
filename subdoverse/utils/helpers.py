def normalize_hostname(host):

    host = host.strip()

    host = host.lower()

    host = host.rstrip(".")

    return host