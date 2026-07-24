import json
from pathlib import Path


def export_json(live_assets, filename, logger):
    """
    Export live assets to JSON.

    Args:
        live_assets (list[dict]):
            Results from httpx.

        filename (str):
            Output JSON filename.

        logger:
            Logger instance.
    """

    output_path = Path(filename)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            live_assets,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info("JSON report generated successfully.")
    logger.info(f"Output file: {output_path.resolve()}")