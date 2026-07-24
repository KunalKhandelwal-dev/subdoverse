import time
import requests


def run_crtsh(domain, config, logger):
    """
    Query crt.sh and return discovered subdomains.

    Args:
        domain (str): Target domain.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        list[str]: Sorted list of discovered subdomains.
    """

    logger.info(f"Querying crt.sh for {domain}")

    url = "https://crt.sh/"

    params = {
        "q": f"%.{domain}",
        "output": "json"
    }

    headers = {
        "User-Agent": "SubEnum/1.0"
    }

    timeout = config["tools"]["crtsh_timeout"]

    retries = config["network"]["retries"]

    for attempt in range(1, retries + 1):

        try:

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )

            response.raise_for_status()

            records = response.json()

            subdomains = set()

            for record in records:

                names = record.get(
                    "name_value",
                    ""
                ).splitlines()

                for hostname in names:

                    hostname = (
                        hostname
                        .strip()
                        .replace("*.", "")
                    )

                    if (
                        hostname
                        and (
                            hostname == domain
                            or hostname.endswith("." + domain)
                        )
                    ):

                        subdomains.add(hostname)

            logger.info(
                f"crt.sh discovered {len(subdomains)} subdomains."
            )

            return sorted(subdomains)

        except requests.exceptions.Timeout:

            logger.warning(
                f"crt.sh timed out "
                f"(attempt {attempt}/{retries})."
            )

        except requests.exceptions.RequestException as exc:

            logger.warning(
                f"crt.sh request failed "
                f"(attempt {attempt}/{retries}): {exc}"
            )

        except ValueError:

            logger.error(
                "crt.sh returned invalid JSON."
            )

            return []

        except Exception as exc:

            logger.exception(
                f"Unexpected crt.sh error: {exc}"
            )

            return []

        if attempt < retries:

            logger.info(
                "Retrying crt.sh..."
            )

            time.sleep(5)

    logger.error(
        "Skipping crt.sh after multiple failed attempts."
    )

    return []