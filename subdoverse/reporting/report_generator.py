from pathlib import Path
from datetime import datetime


def generate_report(
    target,
    statistics,
    filename,
    logger
):
    """
    Generate a professional
    reconnaissance report.
    """

    output = Path(filename)

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report = []

    report.append(
        "# Reconnaissance Report\n"
    )

    report.append(
        f"## Target\n{target}\n"
    )

    report.append(
        f"## Scan Date\n"
        f"{datetime.now()}\n"
    )

    report.append(
        "## Executive Summary\n"
    )

    report.append(
        f"A total of "
        f"{statistics['merged']} "
        f"unique subdomains "
        f"were identified.\n"
    )

    report.append(
        f"{statistics['dns_valid']} "
        f"resolved successfully.\n"
    )

    report.append(
        f"{statistics['live_hosts']} "
        f"live HTTP services "
        f"were detected.\n"
    )

    report.append(
        "\n## Enumeration Summary\n"
    )

    report.append(
        f"- Subfinder: "
        f"{statistics['subfinder']}\n"
    )

    report.append(
        f"- Assetfinder: "
        f"{statistics['assetfinder']}\n"
    )

    report.append(
        f"- Amass: "
        f"{statistics['amass']}\n"
    )

    report.append(
        f"- crt.sh: "
        f"{statistics['crtsh']}\n"
    )

    report.append(
        f"- Unique: "
        f"{statistics['merged']}\n"
    )

    report.append(
        "\n## Top Technologies\n"
    )

    for tech, count in statistics[
        "top_technologies"
    ].items():

        report.append(
            f"- {tech}: {count}\n"
        )

    report.append(
        "\n## Top Web Servers\n"
    )

    for server, count in statistics[
        "top_webservers"
    ].items():

        report.append(
            f"- {server}: {count}\n"
        )

    report.append(
        "\n## HTTP Status Codes\n"
    )

    for code, count in statistics[
        "status_codes"
    ].items():

        report.append(
            f"- {code}: {count}\n"
        )

    report.append(
        "\n## Recommendations\n"
    )

    report.append(
        "- Run Nuclei\n"
    )

    report.append(
        "- Perform Manual Testing\n"
    )

    report.append(
        "- Review Authentication\n"
    )

    report.append(
        "- Enumerate Directories\n"
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "".join(report)
        )

    logger.info(
        f"Report written to {output}"
    )