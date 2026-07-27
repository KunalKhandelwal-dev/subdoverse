# Subdoverse

> **Professional Python-Based Subdomain Enumeration Tool**

Subdoverse is a Python-powered passive subdomain enumeration framework that aggregates results from multiple reconnaissance sources, validates discovered subdomains, identifies live web assets, and generates professional reports in CSV, JSON, and Markdown formats.

---

## Features

- Passive Subdomain Enumeration
- Multiple Enumeration Sources
  - Subfinder
  - Assetfinder
  - Amass
  - crt.sh
- Automatic Result Deduplication
- DNS Validation
- HTTP/HTTPS Validation
- Technology Detection
- CSV Report Generation
- JSON Report Generation
- Markdown Summary Report
- Professional Command Line Interface
- Cross Platform (Windows / Linux)

---

# Project Structure

```
Subdoverse/
│
├── subdoverse/
│   │
│   ├── __init__.py                 # Marks subdoverse as a Python package
│   ├── main.py                     # Application entry point
│   ├── cli.py                      # Command-line argument parser
│   ├── config.py                   # Loads and manages configuration
│   ├── config.json                 # Default project configuration
│   ├── logger.py                   # Logging configuration
│   │
│   ├── runners/
│   │   ├── __init__.py             # Runner package
│   │   ├── subfinder.py            # Executes Subfinder enumeration
│   │   ├── assetfinder.py          # Executes Assetfinder enumeration
│   │   ├── amass.py                # Executes Amass enumeration
│   │   └── crtsh.py                # Queries crt.sh Certificate Transparency logs
│   │
│   ├── validators/
│   │   ├── __init__.py             # Validator package
│   │   ├── dns_validator.py        # Validates discovered subdomains using DNS
│   │   └── http_validator.py       # Identifies live HTTP/HTTPS hosts
│   │
│   ├── exporters/
│   │   ├── __init__.py             # Exporter package
│   │   ├── csv_exporters.py        # Exports scan results to CSV
│   │   └── json_exporters.py       # Exports scan results to JSON
│   │
│   ├── reporting/
│   │   ├── __init__.py             # Reporting package
│   │   └── report_generator.py     # Generates Markdown summary reports
│   │
│   └── utils/
│       ├── __init__.py             # Utility package
│       ├── helpers.py              # Common helper functions
│       ├── merge.py                # Merges and removes duplicate results
│       └── statistics.py           # Generates scan statistics
│
├── install.py                      # Automatic installer for dependencies
├── setup.py                        # Python package configuration
├── pyproject.toml                  # Python build configuration
├── requirements.txt                # Python package dependencies
├── README.md                       # Project documentation
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore rules
```

---

# Requirements

- Python 3.10 or higher
- Git
- Internet Connection

Supported Operating Systems

- Kali Linux
- Ubuntu
- Debian

---

# Installation

Clone the repository

```bash
git clone https://github.com/KunalKhandelwal-dev/Subdoverse.git
```

Move into the project directory

```bash
cd Subdoverse
```

Run the installer

```bash
python3 install.py
```

The installer automatically:

- Checks the operating system
- Verifies Python version
- Checks internet connectivity
- Installs Go (if required)
- Installs Subfinder
- Installs Assetfinder
- Installs httpx
- Installs Amass
- Configures the system PATH
- Installs the Subdoverse package
- Verifies the installation

---

# Verify Installation

```bash
subdoverse --help
```

---

# Usage

Scan a target domain

```bash
subdoverse -d google.com
```

Specify thread count

```bash
subdoverse -d google.com -t 50
```

Export results

```bash
subdoverse -d google.com -f csv
```

```bash
subdoverse -d google.com -f json
```

Specify an output filename

```bash
subdoverse -d google.com -o results
```

Silent mode

```bash
subdoverse -d google.com --silent
```

---

# Reports

Subdoverse generates the following reports after each scan.

```
output/
├── results.csv
├── results.json
└── report.md
```

- **results.csv** – CSV report containing validated results.
- **results.json** – Structured JSON output for automation.
- **report.md** – Markdown report summarizing the scan.

---

# Enumeration Workflow

```
Target Domain
      │
      ▼
Subfinder
      │
      ▼
Assetfinder
      │
      ▼
Amass
      │
      ▼
crt.sh
      │
      ▼
Merge Results
      │
      ▼
DNS Validation
      │
      ▼
HTTP Validation
      │
      ▼
Generate Reports
```

---

# Troubleshooting

### `subdoverse: command not found`

Restart your terminal or reload your shell configuration.

```bash
source ~/.bashrc
```

---

### Installation failed because of Python package restrictions

On newer Kali Linux releases, Python uses PEP 668 protection.

Run:

```bash
python3 install.py
```

The installer automatically handles package installation.

---

### Go tools are not detected

Reload your shell.

```bash
source ~/.bashrc
```

Or restart the terminal.

---

# Contributing

Contributions, feature requests, and bug reports are welcome.

Feel free to open an Issue or submit a Pull Request.

---

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Author

**Kunal Khandelwal**

GitHub: https://github.com/KunalKhandelwal-dev

If you found this project useful, consider giving it a star on GitHub!