import shutil
import subprocess


def run_subfinder(domain, config, logger):
    """
    Run Subfinder and return discovered subdomains.

    Args:
        domain (str): Target domain.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        list[str]: Discovered subdomains.
    """

    tool_path = config["tools"]["subfinder_path"]

    timeout = config["tools"]["subfinder_timeout"]

    logger.info(f"Starting Subfinder for {domain}")

    if shutil.which(tool_path) is None:

        logger.error(
            f"Subfinder executable '{tool_path}' not found."
        )

        return []

    command = [
        tool_path,
        "-d",
        domain,
        "-silent"
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
            f"Subfinder timed out after {timeout} seconds."
        )

        return []

    except Exception as e:

        logger.exception(
            f"Unexpected error while running Subfinder: {e}"
        )

        return []

    if result.returncode != 0:

        logger.error(
            f"Subfinder failed:\n{result.stderr.strip()}"
        )

        return []

    subdomains = []

    for line in result.stdout.splitlines():

        line = line.strip()

        if line:

            subdomains.append(line)

    logger.info(
        f"Subfinder discovered {len(subdomains)} subdomains."
    )

    return subdomains