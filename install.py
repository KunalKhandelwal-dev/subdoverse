import platform
import shutil
import subprocess
import sys
import os
import urllib.request
import sysconfig


def print_header():
    print("=" * 60)
    print("        Subdoverse Installer v1.0")
    print("=" * 60)


def run_command(command):
    """
    Execute a shell command.
    Returns True if successful.
    """

    print(f"\n[>] {command}")

    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:

        if result.stderr:
            print(result.stderr.strip())

        return False

    return True


def command_exists(command):
    """
    Check whether a command exists in PATH.
    """

    return shutil.which(command) is not None


def check_os():
    """
    Detect the operating system.
    """

    os_name = platform.system()

    print(f"[+] Operating System : {os_name}")

    return os_name


def check_python():
    """
    Ensure Python >= 3.10
    """

    version = sys.version_info

    if version.major < 3 or version.minor < 10:

        print("[!] Python 3.10 or higher is required.")
        sys.exit(1)

    print(
        f"[✓] Python {version.major}.{version.minor}.{version.micro}"
    )


def check_internet():
    """
    Verify internet connectivity.
    """

    try:

        urllib.request.urlopen(
            "https://google.com",
            timeout=5
        )

        print("[✓] Internet Connection")

    except Exception:

        print("[!] Internet connection not available.")
        sys.exit(1)

def install_python_package():
    """
    Install the Subdoverse package.
    """

    print("\nInstalling Subdoverse...")

    if sys.prefix != sys.base_prefix:
        command = f'"{sys.executable}" -m pip install .'
    else:
        command = (
            f'"{sys.executable}" -m pip install '
            '--user --break-system-packages .'
        )

    success = run_command(command)

    if not success:
        print("[!] Failed to install Subdoverse.")
        sys.exit(1)

    print("[✓] Subdoverse installed successfully.")

def check_go():
    """
    Check whether Go is installed.
    """

    print("\nChecking Go...")

    if command_exists("go"):

        print("[✓] Go is already installed.")

        return

    print("[!] Go is not installed.")

    install_go()

    if not command_exists("go"):

        print("[!] Go installation verification failed.")

        sys.exit(1)

    print("[✓] Go verified successfully.")

def install_go():
    """
    Install Go.
    """

    print("\nInstalling Go...")

    operating_system = platform.system()

    if operating_system == "Linux":

        command = "sudo apt update && sudo apt install -y golang-go"

    elif operating_system == "Windows":

        command = "winget install GoLang.Go"

    else:

        print("[!] Unsupported Operating System.")

        sys.exit(1)

    success = run_command(command)

    if not success:

        print("[!] Failed to install Go.")

        sys.exit(1)

def get_gopath():
    """
    Return the user's GOPATH.
    """

    try:

        result = subprocess.run(
            ["go", "env", "GOPATH"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.strip()

    except Exception:

        print("[!] Unable to determine GOPATH.")
        sys.exit(1)

def get_python_scripts_dir():
    """
    Return the directory where Python installs command-line scripts.
    """

    return sysconfig.get_path("scripts")

def add_to_current_path(directory):
    """
    Add a directory to the current Python process PATH.
    """

    current_path = os.environ.get("PATH", "")

    if directory not in current_path.split(os.pathsep):

        os.environ["PATH"] = (
            current_path
            + os.pathsep
            + directory
        )

def path_contains(directory):
    """
    Check whether a directory exists as an exact PATH entry.
    """

    return directory in os.environ.get("PATH", "").split(os.pathsep)

def configure_linux_path(paths_to_add):
    """
    Configure PATH on Linux/macOS.
    """

    bashrc = os.path.expanduser("~/.bashrc")

    with open(bashrc, "a") as file:

        for path in paths_to_add:

            file.write(
                f'\nexport PATH="$PATH:{path}"\n'
            )

            add_to_current_path(path)

    print("[✓] PATH updated successfully.")

    print("\nPlease restart your terminal or run:")

    print("source ~/.bashrc")

def configure_windows_path(paths_to_add):
    """
    Configure PATH on Windows.
    """

    for path in paths_to_add:

        add_to_current_path(path)

        run_command(
            f'setx PATH "%PATH%;{path}"'
        )

    print("[✓] PATH updated successfully.")

    print("\nPlease restart Command Prompt or PowerShell.")

def configure_path():
    """
    Configure PATH for Go binaries and Python scripts.
    """

    print("\nConfiguring PATH...")

    paths_to_add = []

    go_bin = os.path.join(get_gopath(), "bin")

    if not path_contains(go_bin):
        paths_to_add.append(go_bin)

    python_scripts = get_python_scripts_dir()

    if not path_contains(python_scripts):
        paths_to_add.append(python_scripts)

    if not paths_to_add:

        print("[✓] PATH already configured.")

        return

    operating_system = platform.system()

    if operating_system == "Windows":

        configure_windows_path(paths_to_add)

    else:

        configure_linux_path(paths_to_add)

def verify_command(command):
    """
    Verify that a command executes successfully.
    """

    print(f"Checking {command:<15}", end="")

    result = subprocess.run(
        f"{command} -h",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:

        print("[✓]")

        return True

    print("[✗]")

    return False

def install_go_tool(tool_name, install_command):
    """
    Install a Go-based tool if it is not already installed.
    """

    print(f"\nChecking {tool_name}...")

    if command_exists(tool_name):
        print(f"[✓] {tool_name} already installed.")
        return

    print(f"[+] Installing {tool_name}...")

    success = run_command(install_command)

    if not success:
        print(f"[!] Failed to install {tool_name}.")
        sys.exit(1)

    # Refresh the current PATH in case a new binary directory was added
    go_bin = os.path.join(get_gopath(), "bin")
    add_to_current_path(go_bin)

    if command_exists("amass"):
        print("[✓] amass installed successfully.")
    else:
        print("[!] amass installation could not be verified.")
        sys.exit(1)

    if command_exists(tool_name):
        print(f"[✓] {tool_name} installed successfully.")
    else:
        print(f"[!] {tool_name} installation could not be verified.")
        sys.exit(1)

def install_subfinder():

    install_go_tool(

        "subfinder",

        "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"

    )

def install_assetfinder():

    install_go_tool(

        "assetfinder",

        "go install github.com/tomnomnom/assetfinder@latest"

    )

def install_httpx():

    install_go_tool(

        "httpx",

        "go install github.com/projectdiscovery/httpx/cmd/httpx@latest"

    )

def install_amass():

    print("\nChecking amass...")

    if command_exists("amass"):

        print("[✓] amass already installed.")

        return

    print("[+] Installing amass...")

    success = run_command(

        "sudo apt update && sudo apt install -y amass"

    )

    if not success:

        print("[!] Failed to install amass.")

        sys.exit(1)

    print("[✓] amass installed successfully.")

def verify_installation():
    """
    Verify that all required tools are installed.
    """

    print("\n" + "=" * 60)
    print("Verifying Installation")
    print("=" * 60)

    tools = [
        "go",
        "subfinder",
        "assetfinder",
        "httpx",
        "amass",
        "subdoverse"
    ]

    failed = False

    for tool in tools:

        if not verify_command(tool):
            failed = True

    if failed:

        print("\n[!] Installation verification failed.")

        sys.exit(1)

    print("\n[✓] All components verified successfully.")



def main():

    print_header()

    operating_system = check_os()

    check_python()

    check_internet()

    check_go()

    configure_path()

    install_subfinder()

    install_assetfinder()

    install_httpx()

    install_amass()

    install_python_package()

    verify_installation()

    print("\nInstallation completed successfully.")


if __name__ == "__main__":
    main()