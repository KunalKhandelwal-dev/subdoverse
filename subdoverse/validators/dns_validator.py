import dns.resolver


def validate_dns(hostname, config, logger):
    """
    Validate a hostname by resolving
    A and AAAA records.

    Args:
        hostname (str): Hostname to validate.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        dict | None
    """

    resolver = dns.resolver.Resolver()

    resolver.timeout = config["network"]["dns_timeout"]

    resolver.lifetime = config["network"]["dns_timeout"]

    result = {
        "hostname": hostname,
        "a_records": [],
        "aaaa_records": []
    }

    for record_type in ["A", "AAAA"]:

        try:

            answers = resolver.resolve(
                hostname,
                record_type
            )

            addresses = [
                answer.to_text()
                for answer in answers
            ]

            if record_type == "A":

                result["a_records"] = addresses

            else:

                result["aaaa_records"] = addresses

        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.Timeout,
            dns.resolver.NoNameservers
        ):

            continue

        except Exception as exc:

            logger.error(
                f"DNS validation failed for "
                f"{hostname}: {exc}"
            )

            continue

    if result["a_records"] or result["aaaa_records"]:

        logger.info(
            f"Valid DNS: {hostname}"
        )

        return result

    logger.warning(
        f"Invalid DNS: {hostname}"
    )

    return None


def validate_all_dns(hostnames, config, logger):
    """
    Validate multiple hostnames.

    Args:
        hostnames (list[str]): Hostnames to validate.
        config (dict): Application configuration.
        logger: Configured logger.

    Returns:
        list[dict]
    """

    valid_hosts = []

    logger.info(
        f"Validating {len(hostnames)} hostnames..."
    )

    for hostname in hostnames:

        result = validate_dns(
            hostname,
            config,
            logger
        )

        if result:

            valid_hosts.append(result)

    logger.info(
        f"DNS validation completed. "
        f"{len(valid_hosts)} valid hosts found."
    )

    return valid_hosts