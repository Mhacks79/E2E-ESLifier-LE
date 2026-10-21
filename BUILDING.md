# Building E2E with PyInstaller (Windows)

This is the build path provided by the source package, with explicit dependency and integrity checks for reviewers.

## 1. Prerequisites

- **Windows x64**. PyInstaller is not a cross-compiler; make the Windows executable on Windows.
- **Python 3.11 x64**, including **Tkinter** (check with `py -3.11 -m tkinter`). Python 3.11 is a known baseline for these sources; other versions may work but are not asserted to reproduce an existing release.
- **.NET SDK 8 or newer** for compiling the bundled C# backend. The produced executable depends on **.NET Runtime 8 or newer** being installed on the computer where E2E runs.
- **PyInstaller**, installed in a dedicated Python environment.
- The exact **`LELightSupport.dll`** expected by the corresponding E2E release. **Not included** in this source repository. Obtain this dependency from the legitimate matching project release; this repository does not supply its compiled binary or native source.

All commands below assume PowerShell and that you have entered the **`E2E-Sources`** directory inside this repository:

```powershell
cd .\E2E-Sources
```

## 2. Create a clean Python build environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\python.exe -m PyInstaller --version
```

Record Python, PyInstaller, and .NET SDK versions in your own review notes if you need a reproducible build environment. PyInstaller's bootloader, Python and dependency version changes can affect the resulting `.exe` byte-for-byte hash even when the Python sources are identical.

## 3. Compile the .NET 8 backend

```powershell
dotnet --version
dotnet restore .\eslifier\backend\ESLifierBackend.csproj --source https://api.nuget.org/v3/index.json
dotnet build .\eslifier\backend\ESLifierBackend.csproj --configuration Release --no-restore
```

The backend references **`Mutagen.Bethesda.Skyrim` version `0.53.1`**, with transitive dependencies resolved by NuGet. The provided `NuGet.Config` clears default package sources, so **the explicit `--source` is important on a new machine**. If you maintain a trusted offline NuGet cache, you can instead restore through that source. The `.NET` project is a *framework-dependent* executable, not a bundled self-contained runtime.

Confirm that `eslifier\backend\bin\Release\net8.0\` exists and contains the compiled backend and dependencies.

## 4. Provide the matching native runtime input

The original PyInstaller script is intentionally configured to expect the native DLL at the following fixed relative path:

```text
E2E-Sources/build/candidate-2026-10-18/LELightSupport.dll
```

For instance, copy the binary you independently obtained from its matching release:

```powershell
New-Item -ItemType Directory -Force .\build\candidate-2026-10-18 | Out-Null
Copy-Item 'C:\PATH\TO\MATCHING\LELightSupport.dll' .\build\candidate-2026-10-18\LELightSupport.dll
(Get-FileHash .\build\candidate-2026-10-18\LELightSupport.dll -Algorithm SHA256).Hash.ToLowerInvariant()
```

**Expected SHA-256 for the current runtime identity in the supplied Python source:**

```text
8163276742248b229889ff071bf02c9d51cdb51e0812b0aebec313352b86a04e
```

That expected digest is defined in [`eslifier/lib/runtime_identity.py`](E2E-Sources/eslifier/lib/runtime_identity.py) **relative to the repository root**. If your DLL hash differs, do not describe it as the matching runtime. Check the exact release/version, and do not attempt to bypass the check by altering the claimed identity.

**Transparency:** The runtime DLL and the C++ code needed to build it are excluded from this published source package. The fact that the Python build script can bundle a DLL does **not** prove that DLL's provenance or trustworthiness. Have Nexus review the corresponding native release separately as needed.

## 5. Run the existing PyInstaller build script

```powershell
.\.venv\Scripts\python.exe .\tools\build_eslifier_exe.py
```

This script invokes PyInstaller with the application's current source entry point:

```text
eslifier/eslifier_app.py
```

It uses the following important options:

| Build option | Purpose |
| --- | --- |
| `--onedir` | Outputs a folder containing `E2E.exe` and its support files, instead of a single self-extracting EXE |
| `--windowed` | Starts the desktop GUI without a console window |
| `--name E2E` | Produces an `E2E` application folder |
| `--paths`, `--hidden-import` | Includes application modules whose imports may be indirect |
| `--add-data` | Copies the built .NET backend, separately supplied runtime DLL, and license notices into the application bundle |
| `--exclude-module` | Excludes designated unused Python modules from the package |

This recipe uses the original project's build code; **it is not a claim that the same binary hash will result on all machines**.

## 6. Verify the resulting folder

Expected layout (abbreviated):

```text
E2E-Sources/
  build/
    exe/
      E2E/
        E2E.exe
        _internal/
          Backend/           # framework-dependent .NET 8 backend
          Runtime/
            LELightSupport.dll
          Licenses/          # licensing notices
          ...                # Python and Tk dependencies
```

The original E2E entry point has a diagnostic option to check all packaged Python module imports:

```powershell
& .\build\exe\E2E\E2E.exe --import-check
```

The expected output includes `imports ok` and a module count if successful. Separately verify the GUI launches on a Windows system with the **.NET Runtime >= 8** installed. Real conversion/in-game testing needs an appropriately configured Skyrim LE/SKSE environment and must be done against safe test files and backups.

Check the built file's hash for reporting to moderation:

```powershell
(Get-FileHash .\build\exe\E2E\E2E.exe -Algorithm SHA256).Hash
```

To distribute this build, compress the **entire** `build\exe\E2E\` folder, not only `E2E.exe`. This is an application release folder, not a source archive.

## 7. Source-verification commands

The original source-only ZIP included `SOURCE_MANIFEST.json` containing SHA-256 hashes of all other members. Paths in that manifest start with `E2E-Sources/` (the original ZIP's top-level folder). Validate it from the **repository root** with:

```powershell
py -3.11 -c "import json,hashlib,pathlib; d=json.loads(pathlib.Path('E2E-Sources/SOURCE_MANIFEST.json').read_text()); bad=[p for p,h in d.items() if not pathlib.Path(p).is_file() or hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h]; print('Mismatched:',bad); raise SystemExit(bool(bad))"
```

No binary trust judgment should be inferred from a passing source-file hash check. The original source package cannot establish the uploaded Nexus binary's hash, and this repository has no native runtime source.