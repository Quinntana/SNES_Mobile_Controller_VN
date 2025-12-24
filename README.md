# SNES Mobile Controller

Turns your mobile browser into a Super Nintendo style controller for Windows. Uses **ViGEmBus** (virtual Xbox 360 controller) and **FastAPI** (WebSockets).

## Prerequisites

1. **Windows 10/11**
2. **ViGEmBus Driver**: [Download & Install](https://github.com/ViGEm/ViGEmBus/releases/latest) (or `winget install ViGEm.ViGEmBus`) -> **REBOOT MIGHT BE
 REQUIRED**
3. **Python 3.10+** & **Poetry**

## Quick Start

1. **Install Dependencies** (once):

    ```powershell
    winget install ViGEm.ViGEmBus
    winget install Libretro.RetroArch
    poetry install
    ```

2. **Run the Server**:

    ```powershell
    .\run.ps1
    ```

## How to Play

1. Start the server.
2. Find your PC's local IP via `ipconfig` (e.g., `192.168.1.5`).
3. Open `http://<YOUR_PC_IP>:3000` on your phone. (e.g., `http://192.168.1.5:3000`)
4. In your emulator (RetroArch, etc.), map the inputs as an **Xbox Controller**.

> **Note**: If connection fails, ensure port **3000** is allowed through Windows Firewall.
