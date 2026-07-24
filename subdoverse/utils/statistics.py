from collections import Counter


def generate_statistics(
    subfinder,
    assetfinder,
    amass,
    crtsh,
    merged,
    validated,
    live_assets,
    duration
):
    """
    Generate reconnaissance statistics.

    Returns
    -------
    dict
    """

    status_counter = Counter()
    technology_counter = Counter()
    server_counter = Counter()
    title_counter = Counter()

    for asset in live_assets:

        status = asset.get(
            "status_code"
        )

        if status is not None:
            status_counter[status] += 1

        for tech in asset.get(
            "tech",
            []
        ):

            technology_counter[tech] += 1

        server = asset.get(
            "webserver"
        )

        if server:
            server_counter[server] += 1

        title = asset.get(
            "title"
        )

        if title:
            title_counter[title] += 1

    statistics = {

        "subfinder":
            len(subfinder),

        "assetfinder":
            len(assetfinder),

        "amass":
            len(amass),

        "crtsh":
            len(crtsh),

        "merged":
            len(merged),

        "dns_valid":
            len(validated),

        "live_hosts":
            len(live_assets),

        "status_codes":
            dict(status_counter),

        "top_technologies":
            dict(
                technology_counter.most_common(10)
            ),

        "top_webservers":
            dict(
                server_counter.most_common(10)
            ),

        "top_titles":
            dict(
                title_counter.most_common(10)
            ),

        "scan_duration":
            round(duration,2)

    }

    return statistics