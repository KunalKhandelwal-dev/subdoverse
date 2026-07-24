import json
from pathlib import Path


def load_config():
    """
    Load configuration from config.json
    located inside the package.
    """

    config_path = (
        Path(__file__)
        .parent
        / "config.json"
    )

    with config_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)