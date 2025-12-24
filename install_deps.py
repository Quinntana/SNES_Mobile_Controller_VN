import subprocess
import shutil
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_winget():
    if not shutil.which("winget"):
        print("Error: 'winget' is not found in PATH. Please install App Installer from the Microsoft Store.")
        sys.exit(1)

def install_package(package_id, package_name):
    print(f"Installing {package_name} ({package_id})...")
    try:
        # -e: exact match
        # --accept-source-agreements: accept store agreements
        # --accept-package-agreements: accept package license
        cmd = ["winget", "install", "-e", "--id", package_id, "--accept-source-agreements", "--accept-package-agreements"]
        subprocess.run(cmd, check=True)
        print(f"Successfully installed/verified {package_name}.")
    except subprocess.CalledProcessError as e:
        # 0x8A15002B = 2316632107 : No update available (already installed)
        if e.returncode == 2316632107 or e.returncode == -1978335189: # check both unsigned/signed
            print(f"{package_name} is already installed and up to date.")
        else:
            print(f"Failed to install {package_name}. Error code: {e.returncode}")
        # Don't exit immediately, try the next one? Or maybe exit. 
        # Usually for setup we might want to continue or warn. 
        # Let's warn and continue.
        print("Continuing...")

def main():
    print("--- SNES Mobile Controller VN Setup Helper ---")
    
    if sys.platform != "win32":
        print("Error: This script is designed for Windows only.")
        sys.exit(1)
    
    check_winget()

    print("Checking for ViGEmBus...")
    # Install ViGEmBus
    install_package("ViGEm.ViGEmBus", "ViGEm Bus Driver")

    print("\nChecking for RetroArch...")
    # Install RetroArch
    install_package("Libretro.RetroArch", "RetroArch")

    print("\nSetup check complete. (Note: winget updates existing packages if a newer version is available).")
    print("You may need to reboot if ViGEmBus was just installed/updated.")

if __name__ == "__main__":
    main()
