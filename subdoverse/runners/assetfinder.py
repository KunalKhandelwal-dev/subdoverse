import shutil
import subprocess


def run_assetfinder(domain, config, logger):
    """
    Run Assetfinder and return discovered subdomains.

    Args:
        domain (str): Target domain.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        list[str]: Discovered subdomains.
    """

    tool_path = config["tools"]["assetfinder_path"]

    timeout = config["tools"]["assetfinder_timeout"]

    logger.info(
        f"Starting Assetfinder for {domain}"
    )

    if shutil.which(tool_path) is None:

        logger.error(
            f"Assetfinder executable '{tool_path}' not found."
        )

        return []

    command = [
        tool_path,
        domain
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        logger.error(
            f"Assetfinder timed out after {timeout} seconds."
        )

        return []

    except Exception as exc:

        logger.exception(
            f"Unexpected error while running Assetfinder: {exc}"
        )

        return []

    if result.returncode != 0:

        logger.error(
            f"Assetfinder failed:\n{result.stderr.strip()}"
        )

        return []

    subdomains = []

    for line in result.stdout.splitlines():

        line = line.strip()

        if not line:
            continue

        if (
            line == domain
            or line.endswith("." + domain)
        ):
            subdomains.append(line)

    subdomains = sorted(set(subdomains))

    logger.info(
        f"Assetfinder discovered {len(subdomains)} subdomains."
    )

    return subdomains