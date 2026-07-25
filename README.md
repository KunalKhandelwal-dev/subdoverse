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
│   ├── exporters/
│   ├── reporting/
│   ├── runners/
│   ├── utils/
│   ├── validators/
│   ├── cli.py
│   ├── config.py
│   ├── config.json
│   ├── logger.py
│   ├── __init__.py
│   └── main.py
│
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── pyproject.toml
```

---

# Requirements

## Operating System

- Kali Linux (Recommended)
- Ubuntu
- Debian
- Windows 10/11

---

## Python

Python 3.10+

Verify:

```bash
python3 --version
```

---

## Git

Verify:

```bash
git --version
```

---

# Installation Guide (Kali Linux)

## Step 1 — Update System

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2 — Install Required Packages

```bash
sudo apt install git python3 python3-pip python3-venv golang amass -y
```

Verify:

```bash
python3 --version
git --version
go version
amass -version
```

---

## Step 3 — Clone Repository

```bash
git clone https://github.com/KunalKhandelwal-dev/Subdoverse.git
```

Enter the project directory

```bash
cd Subdoverse
```

---

## Step 4 — Create Virtual Environment

```bash
python3 -m venv venv
```

Activate it

```bash
source venv/bin/activate
```

Your terminal should now look like

```text
(venv)
```

---

## Step 5 — Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## Step 6 — Install Python Dependencies

```bash
pip install .
```

or for development

```bash
pip install -e .
```

---

# Installing External Enumeration Tools

Subdoverse depends on several external reconnaissance tools.

---

## 1. Subfinder

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

Verify

```bash
subfinder -h
```

---

## 2. Assetfinder

```bash
go install github.com/tomnomnom/assetfinder@latest
```

Verify

```bash
assetfinder -h
```

---

## 3. httpx

```bash
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

Verify

```bash
httpx -h
```

---

## 4. Amass

Already installed earlier using

```bash
sudo apt install amass -y
```

Verify

```bash
amass -h
```

---

## 5. crt.sh

No installation is required.

Subdoverse queries the public Certificate Transparency logs available at:

https://crt.sh

An active internet connection is required for crt.sh enumeration.

---

# Add Go Tools to PATH

If Subfinder, Assetfinder, or httpx are not recognized, add the Go binary directory to your PATH.

```bash
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
```

Reload the shell

```bash
source ~/.bashrc
```

Verify

```bash
subfinder -h
assetfinder -h
httpx -h
```

---

# Verify Installation

Check that Subdoverse was installed successfully.

```bash
subdoverse --help
```

You should see the command line help menu.

---

# Running Your First Scan

Example

```bash
subdoverse -d google.com
```

Another example

```bash
subdoverse -d example.com
```

---

# Generated Reports

After a successful scan, the following reports are generated.

```
output/

results.csv

results.json

report.md
```

---

# CSV Report

Contains

- Live Host
- Status Code
- Technologies
- Title
- URL

---

# JSON Report

Contains complete structured scan results for automation or further processing.

---

# Markdown Report

Contains

- Scan Summary
- Statistics
- Live Assets
- Technologies
- Status Code Distribution

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
Technology Detection
      │
      ▼
Generate Reports
```

---

# Troubleshooting

## "subfinder: command not found"

Install Subfinder

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

---

## "assetfinder: command not found"

```bash
go install github.com/tomnomnom/assetfinder@latest
```

---

## "httpx: command not found"

```bash
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

---

## "amass: command not found"

```bash
sudo apt install amass -y
```

---

## Go binaries are not found

```bash
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

---

## Python dependencies are missing

```bash
pip install -r requirements.txt
```

or

```bash
pip install .
```

---

# Contributing

Contributions, feature requests, and bug reports are welcome.

Feel free to open an Issue or submit a Pull Request.

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Author

**Kunal Khandelwal**

GitHub:

https://github.com/KunalKhandelwal-dev

---

⭐ If you found this project useful, consider giving it a star on GitHub!
