import json
import shutil
import subprocess
import tempfile
import os
import sys


def validate_http(hostnames, config, logger):
    """
    Probe hostnames using ProjectDiscovery httpx.

    Args:
        hostnames (list[str]): Valid DNS hostnames.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        list[dict]
    """

    tool_path = config["tools"]["httpx_path"]

    timeout = config["tools"]["httpx_timeout"]

    threads = config["performance"]["threads"]

    logger.info(
        f"Starting HTTP validation for {len(hostnames)} hosts."
    )

    if shutil.which(tool_path) is None:

        logger.error(
            f"httpx executable '{tool_path}' not found."
        )

        return []

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    )

    try:

        for host in hostnames:

            temp_file.write(host + "\n")

        temp_file.close()

        command = [
            tool_path,
            "-l",
            temp_file.name,
            "-silent",
            "-json",
            "-title",
            "-status-code",
            "-ip",
            "-web-server",
            "-follow-redirects",
            "-threads",
            str(threads)
        ]

        kwargs = {
            "capture_output": True,
            "text": True,
            "timeout": timeout
        }

        if sys.platform == "win32":

            startupinfo = subprocess.STARTUPINFO()

            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            kwargs["startupinfo"] = startupinfo

            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(
            command,
            **kwargs
        )

        if result.returncode != 0:

            logger.error(
                f"httpx failed:\n{result.stderr.strip()}"
            )

            return []

        live_hosts = []

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            try:

                live_hosts.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:

                logger.warning(
                    f"Invalid JSON received from httpx:\n{line}"
                )

        logger.info(
            f"httpx discovered {len(live_hosts)} live web assets."
        )

        return live_hosts

    except subprocess.TimeoutExpired:

        logger.error(
            f"httpx timed out after {timeout} seconds."
        )

        return []

    except Exception as exc:

        logger.exception(
            f"Unexpected error while running httpx: {exc}"
        )

        return []

    finally:

        if os.path.exists(temp_file.name):

            os.remove(temp_file.name)