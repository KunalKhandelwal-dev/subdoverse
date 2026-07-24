import csv
from pathlib import Path

def export_csv(live_assets, filename, logger):
    """
    Export live assets to a CSV report.

    Args:
        live_assets (list[dict]): Results from httpx.
        filename (str): Output file path.
        logger: Logger instance.
    """

    output_path = Path(filename)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "Host",
        "URL",
        "IP",
        "Status",
        "Title",
        "Web Server",
        "Technologies"
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for asset in live_assets:
            writer.writerow({
                "Host":
                    asset.get("host", ""),

                "URL":
                    asset.get("url", ""),

                "IP":
                    asset.get("ip", ""),

                "Status":
                    asset.get(
                        "status_code",
                        ""
                    ),

                "Title":
                    asset.get(
                        "title",
                        ""
                    ),

                "Web Server":
                    asset.get(
                        "webserver",
                        ""
                    ),

                "Technologies":
                    ", ".join(
                        asset.get(
                            "tech",
                            []
                        )
                    )
            })

    logger.info("CSV report generated successfully.")
    logger.info(f"Output file: {output_path.resolve()}")





