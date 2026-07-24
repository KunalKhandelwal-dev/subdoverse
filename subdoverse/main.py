import time
from pathlib import Path

from subdoverse.cli import parse_arguments
from subdoverse.config import load_config
from subdoverse.logger import setup_logger

from subdoverse.runners.subfinder import run_subfinder
from subdoverse.runners.assetfinder import run_assetfinder
from subdoverse.runners.amass import run_amass
from subdoverse.runners.crtsh import run_crtsh

from subdoverse.validators.dns_validator import validate_all_dns
from subdoverse.validators.http_validator import validate_http

from subdoverse.utils.merge import merge_results
from subdoverse.utils.statistics import generate_statistics

from subdoverse.exporters.csv_exporters import export_csv
from subdoverse.exporters.json_exporters import export_json

from subdoverse.reporting.report_generator import generate_report


TOTAL_STAGES = 8


def print_banner():

    print("=" * 60)
    print("              SubDoVerse v1.0.0")
    print("     Professional Subdomain Enumeration Tool")
    print("=" * 60)


def print_stage(stage, title):

    print("\n" + "-" * 60)
    print(f"[{stage}/{TOTAL_STAGES}] {title}")
    print("-" * 60)


def print_success(message):

    print(f"[✓] {message}")


def main():

    overall_start = time.time()

    args = parse_arguments()

    config = load_config()

    logger = setup_logger(config)

    output_dir = Path(
        config["output"]["directory"]
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print_banner()

    print(f"\nTarget   : {args.domain}")
    print(
        f"Started  : {time.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    logger.info(
        f"Scanning target {args.domain}"
    )

    # ----------------------------------------------------

    print_stage(1, "Running Subfinder")

    start = time.time()

    subfinder_results = run_subfinder(
        args.domain,
        config,
        logger
    )

    print_success(
        f"{len(subfinder_results)} subdomains "
        f"({time.time()-start:.2f}s)"
    )

    # ----------------------------------------------------

    print_stage(2, "Running Assetfinder")

    start = time.time()

    assetfinder_results = run_assetfinder(
        args.domain,
        config,
        logger
    )

    print_success(
        f"{len(assetfinder_results)} subdomains "
        f"({time.time()-start:.2f}s)"
    )

    # ----------------------------------------------------

    print_stage(3, "Running Amass")

    start = time.time()

    amass_results = run_amass(
        args.domain,
        config,
        logger
    )

    print_success(
        f"{len(amass_results)} subdomains "
        f"({time.time()-start:.2f}s)"
    )

    # ----------------------------------------------------

    print_stage(4, "Querying crt.sh")

    start = time.time()

    crtsh_results = run_crtsh(
        args.domain,
        config,
        logger
    )

    print_success(
        f"{len(crtsh_results)} subdomains "
        f"({time.time()-start:.2f}s)"
    )

    # ----------------------------------------------------

    print_stage(5, "Merging Results")

    start = time.time()

    all_subdomains = merge_results(
        [
            subfinder_results,
            assetfinder_results,
            amass_results,
            crtsh_results
        ]
    )

    print_success(
        f"{len(all_subdomains)} unique subdomains "
        f"({time.time()-start:.2f}s)"
    )

    # ----------------------------------------------------

    print_stage(6, "DNS Validation")

    start = time.time()

    validated_dns = validate_all_dns(
        all_subdomains,
        config,
        logger
    )

    print_success(
        f"{len(validated_dns)} valid hosts "
        f"({time.time()-start:.2f}s)"
    )

    hostnames = [
        host["hostname"]
        for host in validated_dns
    ]

    # ----------------------------------------------------

    print_stage(7, "HTTP Validation")

    start = time.time()

    live_assets = validate_http(
        hostnames,
        config,
        logger
    )

    print_success(
        f"{len(live_assets)} live web assets "
        f"({time.time()-start:.2f}s)"
    )

    # ----------------------------------------------------

    print_stage(8, "Generating Reports")

    start = time.time()

    export_csv(
        live_assets,
        config["output"]["csv"],
        logger
    )

    export_json(
        live_assets,
        config["output"]["json"],
        logger
    )

    duration = time.time() - overall_start

    stats = generate_statistics(
        subfinder_results,
        assetfinder_results,
        amass_results,
        crtsh_results,
        all_subdomains,
        validated_dns,
        live_assets,
        duration
    )

    generate_report(
        target=args.domain,
        statistics=stats,
        filename=config["output"]["report"],
        logger=logger
    )

    print_success(
        f"Reports generated ({time.time()-start:.2f}s)"
    )

    logger.info(
        "Scan completed successfully."
    )

    print("\n" + "=" * 60)
    print("                 Scan Completed")
    print("=" * 60)

    print(f"\nTarget            : {args.domain}")
    print(f"Subfinder         : {stats['subfinder']}")
    print(f"Assetfinder       : {stats['assetfinder']}")
    print(f"Amass             : {stats['amass']}")
    print(f"crt.sh            : {stats['crtsh']}")
    print(f"Unique            : {stats['merged']}")
    print(f"DNS Valid         : {stats['dns_valid']}")
    print(f"Live HTTP         : {stats['live_hosts']}")
    print(f"Duration          : {duration:.2f} seconds")

    print("\nTop Technologies")

    if stats["top_technologies"]:

        for tech, count in stats[
            "top_technologies"
        ].items():

            print(
                f"  • {tech:<20} {count}"
            )

    else:

        print("  None")

    print("\nHTTP Status Codes")

    if stats["status_codes"]:

        for code, count in stats[
            "status_codes"
        ].items():

            print(
                f"  • {code:<20} {count}"
            )

    else:

        print("  None")

    print("\nGenerated Reports")

    print(f"  ✓ {config['output']['csv']}")
    print(f"  ✓ {config['output']['json']}")
    print(f"  ✓ {config['output']['report']}")

    print("\nThank you for using SubdoVerse!")

    print("=" * 60)


if __name__ == "__main__":
    main()