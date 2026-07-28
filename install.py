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
        print(f"[!] Exit code: {result.returncode}")
        if result.stderr:
            print(result.stderr.strip())
        return False

    return True


def command_exists(command):
    """
    Check whether a command exists in PATH.
    """
    return shutil.which(command) is not None


def is_projectdiscovery_httpx():
    """
    Check if httpx is installed and is specifically the ProjectDiscovery version.
    """
    try:
        result = subprocess.run(
            ["httpx", "-l"],
            capture_output=True,
            text=True,
        )
        output = result.stdout.lower() + result.stderr.lower()
        return "flag needs an argument: -l" in output or "usage:" in output
    except Exception:
        return False


def is_valid_tool(tool_name):
    """
    Verify if a tool is actually installed and is the correct version/flavor.
    """
    if tool_name == "httpx":
        return is_projectdiscovery_httpx()
    
    return command_exists(tool_name)


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

    print(f"[✓] Python {version.major}.{version.minor}.{version.micro}")


def check_internet():
    """
    Verify internet connectivity.
    """
    try:
        urllib.request.urlopen("https://google.com", timeout=5)
        print("[✓] Internet Connection")
    except Exception:
        print("[!] Internet connection not available.")
        sys.exit(1)


def check_pipx():
    """
    Check whether pipx is installed.
    Install it through apt if missing.
    """
    print("\nChecking pipx...")

    if command_exists("pipx"):
        print("[✓] pipx is already installed.")
        return

    print("[+] pipx is not installed.")
    print("[+] Installing pipx...")

    success = run_command(
        "sudo apt update && sudo apt install -y pipx"
    )

    if not success:
        print("[!] Failed to install pipx.")
        sys.exit(1)

    if not command_exists("pipx"):
        print("[!] pipx installation could not be verified.")
        sys.exit(1)

    print("[✓] pipx installed successfully.")


def configure_pipx_path():
    """
    Ensure the pipx application directory is available in PATH.
    """
    print("\nConfiguring pipx PATH...")

    success = run_command(
        "pipx ensurepath"
    )

    if not success:
        print("[!] pipx PATH configuration failed.")
        sys.exit(1)

    # pipx normally exposes applications here on Linux.
    user_bin = os.path.join(
        os.path.expanduser("~"),
        ".local",
        "bin"
    )

    add_to_current_path(user_bin)

    print(f"[✓] pipx application directory configured: {user_bin}")


def install_subdoverse():
    """
    Install Subdoverse as an isolated CLI application using pipx.
    """
    print("\nInstalling Subdoverse...")

    project_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    command = [
        "pipx",
        "install",
        project_dir,
        "--force"
    ]

    print("\n[>] " + " ".join(command))

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            print(result.stdout.strip())

        if result.returncode != 0:
            if result.stderr.strip():
                print(result.stderr.strip())
            
            print("[!] Failed to install Subdoverse using pipx.")
            sys.exit(1)

    except Exception as exc:
        print(f"[!] Unexpected pipx installation error: {exc}")
        sys.exit(1)

    # Make pipx application directory available
    # immediately to the running installer.
    user_bin = os.path.join(
        os.path.expanduser("~"),
        ".local",
        "bin"
    )

    add_to_current_path(user_bin)

    print("[✓] Subdoverse installed successfully.")


def verify_subdoverse():
    """
    Verify the Subdoverse CLI installed by pipx.
    """
    print("Checking subdoverse".ljust(25), end="")

    executable = shutil.which("subdoverse")

    if executable is None:
        print("[✗]")
        return False

    try:
        result = subprocess.run(
            [executable, "--help"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode == 0:
            print("[✓]")
            return True

    except (subprocess.SubprocessError, OSError):
        pass

    print("[✗]")
    return False


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
    norm_dir = os.path.normpath(directory)
    norm_paths = [os.path.normpath(p) for p in current_path.split(os.pathsep) if p]
    
    if norm_dir not in norm_paths:
        os.environ["PATH"] = current_path + os.pathsep + directory


def path_contains(directory):
    """
    Check whether a directory exists as an exact PATH entry (normalized).
    """
    norm_dir = os.path.normpath(directory)
    norm_paths = [os.path.normpath(p) for p in os.environ.get("PATH", "").split(os.pathsep) if p]
    
    return norm_dir in norm_paths


def get_shell_config():
    """
    Return the user's shell configuration file.
    """
    shell = os.environ.get("SHELL", "")
    home = os.path.expanduser("~")

    if shell.endswith("bash"):
        return os.path.join(home, ".bashrc")
    elif shell.endswith("zsh"):
        return os.path.join(home, ".zshrc")
    else:
        return os.path.join(home, ".profile")


def shell_config_contains(shell_config, directory):
    """
    Check whether the shell configuration file already contains the PATH entry.
    """
    if not os.path.exists(shell_config):
        return False

    with open(shell_config, "r") as file:
        content = file.read()

    export_line = f'export PATH="$PATH:{directory}"'
    return export_line in content


def configure_linux_path(paths_to_add):
    """
    Configure PATH on Linux/macOS.
    """
    shell_config = get_shell_config()

    with open(shell_config, "a") as file:
        for path in paths_to_add:
            if not shell_config_contains(shell_config, path):
                file.write(f'\nexport PATH="$PATH:{path}"\n')
            add_to_current_path(path)

    print("[✓] PATH updated successfully.")
    print("\nPlease restart your terminal or run:")
    print(f"source {shell_config}")


def configure_windows_path(paths_to_add):
    """
    Configure PATH on Windows.
    """
    for path in paths_to_add:
        add_to_current_path(path)
        run_command(f'setx PATH "%PATH%;{path}"')

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


def verify_command(tool_name, cmd):
    """
    Verify that a command executes successfully.
    """
    print(f"Checking {tool_name}".ljust(25), end="")

    result = subprocess.run(
        cmd,
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
    Install a generic Go-based tool if it is not already installed.
    """
    print(f"\nChecking {tool_name}...")

    if is_valid_tool(tool_name):
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

    # Verify that go install actually created the binary where we expect
    exe_name = f"{tool_name}.exe" if platform.system() == "Windows" else tool_name
    binary_path = os.path.join(go_bin, exe_name)

    if os.path.exists(binary_path) or is_valid_tool(tool_name):
        print(f"[✓] {tool_name} installed successfully.")
    else:
        print(f"[!] {tool_name} installation could not be verified.")
        sys.exit(1)


def install_subfinder():
    install_go_tool(
        "subfinder",
        "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && go clean -cache"
    )


def install_assetfinder():
    install_go_tool(
        "assetfinder",
        "go install github.com/tomnomnom/assetfinder@latest && go clean -cache"
    )


def install_httpx():
    """
    Custom installer for httpx to ensure it's the ProjectDiscovery version.
    """
    print("\nChecking httpx...")

    if is_valid_tool("httpx"):
        print("[✓] ProjectDiscovery httpx already installed.")
        return

    print("[+] Installing ProjectDiscovery httpx...")
    
    install_cmd = "go install github.com/projectdiscovery/httpx/cmd/httpx@latest && go clean -cache"
    success = run_command(install_cmd)

    if not success:
        print("[!] Failed to install httpx.")
        sys.exit(1)

    # Refresh the current PATH
    go_bin = os.path.join(get_gopath(), "bin")
    add_to_current_path(go_bin)

    # Validate that go install created the binary
    exe_name = "httpx.exe" if platform.system() == "Windows" else "httpx"
    binary_path = os.path.join(go_bin, exe_name)

    if os.path.exists(binary_path) or is_valid_tool("httpx"):
        print("[✓] ProjectDiscovery httpx installed successfully.")
    else:
        print("[!] httpx installation could not be verified.")
        sys.exit(1)


def install_amass():
    print("\nChecking amass...")

    if is_valid_tool("amass"):
        print("[✓] amass already installed.")
        return

    print("[+] Installing amass...")
    success = run_command("sudo apt update && sudo apt install -y amass")

    if not success:
        print("[!] Failed to install amass.")
        sys.exit(1)

    print("[✓] amass installed successfully.")


def verify_installation():
    """
    Verify that all required components are available.
    """
    print("\n" + "=" * 60)
    print("Verifying Installation")
    print("=" * 60)

    verification_commands = {
        "go": "go version",
        "subfinder": "subfinder -version",
        "assetfinder": "assetfinder -h",
        "amass": "amass -version",
    }

    failed = False

    for tool, command in verification_commands.items():
        if not verify_command(tool, command):
            failed = True

    # httpx requires special verification because
    # another application may also use the name "httpx".
    print("Checking httpx".ljust(25), end="")

    if is_projectdiscovery_httpx():
        print("[✓]")
    else:
        print("[✗]")
        failed = True

    if not verify_subdoverse():
        failed = True

    if failed:
        print("\n[!] Installation verification failed.")
        sys.exit(1)

    print("\n[✓] All components verified successfully.")


def main():
    print_header()

    check_os()
    check_python()
    check_internet()

    # Go environment
    check_go()
    configure_path()

    # External reconnaissance tools
    install_subfinder()
    install_assetfinder()
    install_httpx()
    install_amass()

    # Python CLI environment
    check_pipx()
    configure_pipx_path()
    install_subdoverse()

    # Final verification
    verify_installation()

    print("\n" + "=" * 60)
    print("Installation completed successfully.")
    print("=" * 60)

    print("\nSubdoverse is ready to use.")
    print("\nExample:")
    print("subdoverse -d example.com")


if __name__ == "__main__":
    main()