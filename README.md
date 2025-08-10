# SNESMobileControllerVN

**Mobile browser SNES-style controller that maps touch/button events to a Windows virtual gamepad (ViGEm) using a FastAPI WebSocket server.**

**Author:** Quinntana

---

## Quickstart (for a new user — shortest path)
1. Install prerequisites (Python, Poetry, ViGEmBus). See *Prerequisites* below.
2. Clone this repo and `cd` into it.
3. `poetry install`
4. Install ViGEmBus driver on Windows and ensure it is running.
5. Run the server:
```powershell
# from project root (Windows PowerShell)
poetry run uvicorn console_controller.main:app --app-dir src --host 0.0.0.0 --port 3000 --reload
```
6. On your phone (same LAN) open `http://<PC-LAN-IP>:3000` and use the on-screen controller.
7. In your emulator (RetroArch / DuckStation), select **XInput** as the input device so the virtual Xbox controller is recognized.

## Detailed Setup for a New User (step-by-step)

### 1) Prerequisites (Windows)
- **Windows 10/11 (64-bit)** — required for ViGEmBus driver + vgamepad.
- **Python 3.13+** (or latest stable 3.x). Install from python.org.
- **Poetry** (recommended) — install via:
```powershell
pip install poetry
```
- **Git** — to clone/push the repo.
- **ViGEmBus driver** — install the ViGEmBus driver for Windows (search "ViGEmBus installer" or the ViGEm project releases on GitHub). After install, reboot if required.
- Optional: a game emulator (RetroArch / DuckStation), and a gamepad tester app to verify virtual device presence.

---

### 2) Clone & Install
```bash
# clone (SSH or HTTPS)
git clone git@github.com:<your-username>/SNESMobileControllerVN.git
cd SNESMobileControllerVN

# install dependencies (Poetry)
poetry install
```
If you prefer not to use Poetry:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell
pip install --upgrade pip
pip install fastapi uvicorn vgamepad
```

**If your imports fail**, run uvicorn with `--app-dir src` or set PYTHONPATH to `src`:
```powershell
# option A (recommended)
poetry run uvicorn console_controller.main:app --app-dir src --host 0.0.0.0 --port 3000 --reload

# option B (PowerShell)
$env:PYTHONPATH = "src"
poetry run uvicorn src.console_controller.main:app --host 0.0.0.0 --port 3000 --reload
```

---

### 3) Install ViGEmBus (virtual gamepad driver)
- Download and run the ViGEmBus installer for Windows (from the ViGEm GitHub repo/releases).
- Reboot if required.
- The `vgamepad` Python package interacts with this driver to create a virtual XInput controller.

Install `vgamepad` is handled by Poetry (`poetry install`) if listed as dependency. If using pip:
```powershell
pip install vgamepad
```

---

### 4) Configure Windows Firewall (allow port 3000)
Run PowerShell *as Administrator* and run:
```powershell
New-NetFirewallRule -DisplayName "SNESMobileControllerVN" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```
Or open **Windows Security → Firewall & network protection → Allow an app through firewall** and add the Python/UVicorn process or explicitly open port 3000.

---

### 5) Start the Server
From project root (PowerShell):
```powershell
poetry run uvicorn console_controller.main:app --app-dir src --host 0.0.0.0 --port 3000 --reload
```
If you used a plain venv:
```powershell
.venv\Scripts\Activate.ps1
uvicorn src.console_controller.main:app --host 0.0.0.0 --port 3000 --reload
```

**Confirm**: Visit `http://<PC-IP>:3000` from a phone on the same Wi‑Fi. The UI should connect and show "Connected".

---

### 6) Emulator / Game Setup
- Open RetroArch.
- Set core to SNES 9x.
- Download ROM to `downloads` folder "C:\RetroArch-Win64\downloads"
- In "Game Controllers" in Windows, you should see the virtual Xbox pad created by ViGEm. Use it in-game.

---

### 7) Testing & Debugging
- If you do **not** see the virtual controller in Windows:
  - Confirm ViGEmBus is installed and driver service is running.
  - Reboot Windows after installing ViGEmBus.
  - Run the server as Administrator (if necessary).
- If the phone cannot connect:
  - Check PC and phone are on the same network.
  - Confirm firewall rule exists or temporarily disable firewall for testing.
  - Ensure correct PC LAN IP is used (run `ipconfig` to confirm).
- If Python import errors occur:
  - Use `--app-dir src` when running uvicorn or set PYTHONPATH to `src`.

---

## Troubleshooting quick list
- **Gamepad not detected**: ViGEmBus missing or not running → reinstall + reboot.
- **WebSocket fails**: Wrong IP/port or firewall blocking → check `ipconfig`, firewall rules.
- **Multiple controllers**: Each connection may create a new virtual pad. Reconnect logic is in `src/console_controller/main.py`.

---

## Contributing & License
- `GPL3.0` license. Add `LICENSE` file.
- Contributions: Fork → branch → PR. Add clear testing steps.

---

## Contact
Author: **Quinntana** — open to issues/PRs on the GitHub repo.

