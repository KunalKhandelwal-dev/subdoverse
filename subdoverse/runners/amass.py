import shutil
import subprocess
import sys


def run_amass(domain, config, logger):
    """
    Run Amass in passive mode.

    Args:
        domain (str): Target domain.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        list[str]: Discovered subdomains.
    """

    tool_path = config["tools"]["amass_path"]

    timeout = config["tools"]["amass_timeout"]

    logger.info(
        f"Starting Amass for {domain}"
    )

    if shutil.which(tool_path) is None:

        logger.error(
            f"Amass executable '{tool_path}' not found."
        )

        return []

    command = [
        tool_path,
        "enum",
        "-passive",
        "-d",
        domain
    ]

    kwargs = {
        "capture_output": True,
        "text": True,
        "timeout": timeout
    }

    # Hide console window on Windows
    if sys.platform == "win32":

        startupinfo = subprocess.STARTUPINFO()

        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        kwargs["startupinfo"] = startupinfo

        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    try:

        result = subprocess.run(
            command,
            **kwargs
        )

    except subprocess.TimeoutExpired:

        logger.error(
            f"Amass timed out after {timeout} seconds."
        )

        return []

    except Exception as exc:

        logger.exception(
            f"Unexpected error while running Amass: {exc}"
        )

        return []

    if result.returncode != 0:

        logger.error(
            f"Amass failed:\n{result.stderr.strip()}"
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
        f"Amass discovered {len(subdomains)} subdomains."
    )

    return subdomains