import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Python Subdomain Emuneration Tool"
    )

    parser.add_argument(
        "-d",
        "--domain",
        required = True,
        help = "Target Domain"
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=50,
        help="Worker Threads"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output Filename"
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Export Format"
    )

    parser.add_argument(
        "--silent",
        action="store_true",
        help="Silent mode"
    )

    return parser.parse_args()