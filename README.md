> **Publication status (2026-10-21):** The source tree is being uploaded. The files under `E2E-Sources/` described below are **not yet available in this repository**. The linked paths will work after the complete archive is pushed. Please do not treat this partial repository as sufficient for source review.

# E2E — ESLifier for Skyrim Legendary Edition

**Source disclosure for Nexus Mods moderation** · **Authors: Mhacks79 & Deno46** · **GPL-3.0**

This repository publishes the **E2E (ESLifier LE) Python/Tk desktop application**, its Python modules and tests, its C#/.NET 8 plugin-conversion backend, its **PyInstaller build script**, dependency notices, and archived third-party dependency sources. It is intended to make the **application-side source and packaging process** inspectable by the Nexus Mods moderation team and other reviewers.

> **Scope / important limitation:** This is **not the complete source code for the Skyrim runtime**. The `LELightSupport.dll` SKSE plugin, its native C++ implementation and SDK, and compiled release binaries are **not included**. Building the full E2E distribution requires supplying the **matching, separately distributed `LELightSupport.dll`**. A review of this repository alone cannot certify the native DLL or prove that a particular uploaded binary was built from these exact files.

## What the software does

E2E is a Windows desktop utility for **Skyrim Legendary Edition (1.9.32.0.8)** and the **SKSE 1.7.3**-based LE Light Support environment. It scans plugins, determines ESL conversion eligibility, prepares and installs converted plugin files with backup/restore support, and can process associated assets. The core user interface is written in Python/Tkinter; a .NET 8 command-line backend performs plugin record operations.

The application is an **on-demand modding tool**, not an automatic game patch or general system installer. Reviewers should inspect the implementation instead of relying on any blanket safety claims.

## Where to inspect the source

| Component | Path |
| --- | --- |
| GUI and application entry point | [`E2E-Sources/eslifier/eslifier_app.py`](E2E-Sources/eslifier/eslifier_app.py), [`eslifier_gui.py`](E2E-Sources/eslifier/eslifier_gui.py) |
| Conversion logic | [`E2E-Sources/eslifier/eslifier.py`](E2E-Sources/eslifier/eslifier.py), [`lib/`](E2E-Sources/eslifier/lib/) |
| C#/.NET backend | [`E2E-Sources/eslifier/backend/`](E2E-Sources/eslifier/backend/) |
| Executable packaging command | [`E2E-Sources/tools/build_eslifier_exe.py`](E2E-Sources/tools/build_eslifier_exe.py) |
| Python tests and synthetic fixtures | [`E2E-Sources/eslifier/tests/`](E2E-Sources/eslifier/tests/) |
| Third-party licences and notices | [`E2E-Sources/licenses/`](E2E-Sources/licenses/) |
| Archived third-party sources | [`E2E-Sources/distribution-sources/`](E2E-Sources/distribution-sources/) |
| Checksums of the original source package | [`E2E-Sources/SOURCE_MANIFEST.json`](E2E-Sources/SOURCE_MANIFEST.json) |

The `E2E-Sources/` tree reproduces the supplied **source-only ZIP** without deliberate edits to its tracked source files. Files at the repository root provide publication/reviewer documentation and a convenience upload script. See [`SOURCE_PROVENANCE.md`](SOURCE_PROVENANCE.md).

## Build the Windows E2E executable

Detailed, auditable instructions: **[BUILDING.md](BUILDING.md)**.

Requirements on **Windows x64**: **Python 3.11 with Tkinter**, **.NET SDK 8 or later** and the **matching `LELightSupport.dll`**. The generated E2E program also needs the **.NET Runtime 8 or later** on the end user's computer. The build uses PyInstaller `--onedir --windowed` (not `--onefile`).

From PowerShell, in the source folder:

```powershell
cd .\E2E-Sources
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pyinstaller

dotnet restore .\eslifier\backend\ESLifierBackend.csproj --source https://api.nuget.org/v3/index.json
dotnet build .\eslifier\backend\ESLifierBackend.csproj --configuration Release --no-restore

# Copy the matching DLL to: .\build\candidate-2026-10-18\LELightSupport.dll
# Verify its SHA-256 (exact value in BUILDING.md) before continuing.

.\.venv\Scripts\python.exe .\tools\build_eslifier_exe.py
```

**Result:** `E2E-Sources/build/exe/E2E/E2E.exe` plus `_internal/` dependencies. **The entire `E2E/` folder must be distributed together.** The final step will fail unless the missing native DLL is provided; the missing file is not silently downloaded or generated.

## For Nexus Mods reviewers

Read **[NEXUS_MODERATION.md](NEXUS_MODERATION.md)** for a short, copyable explanation of the artifact's structure, the missing native DLL, exact verification points, and steps to reproduce the packaging process. This repository provides transparency for an **independent assessment**, not a request to disable security checks.

## License and credits

Application sources are provided with [`E2E-Sources/LICENSE`](E2E-Sources/LICENSE) (GPL-3.0). Credit: **Mhacks79 & Deno46**. Third-party components may have their **own** licensing terms, listed under `E2E-Sources/licenses/`; consult them before redistribution. `E2E-Sources/distribution-sources/` contains preserved third-party source archives, not additional E2E executables.