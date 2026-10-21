# Nexus Mods moderation — E2E source and packaging disclosure

**Software:** E2E / ESLifier LE for Skyrim Legendary Edition  
**Authors:** Mhacks79 and Deno46  
**License of application source:** GPL-3.0 (third-party notices included)

## Purpose of this repository

This repository publishes the application-side sources for reviewers inspecting a Windows executable distributed as **`E2E.exe`** (and its accompanying `E2E/` support directory). Its goal is to make the origin, behaviour, third-party dependencies and PyInstaller packaging steps transparent as part of a normal Nexus Mods safety review.

## Review map

- **Program entry point and runtime check:** `E2E-Sources/eslifier/eslifier_app.py`
- **Tk GUI:** `E2E-Sources/eslifier/eslifier_gui.py`
- **Conversion and filesystem operations:** `E2E-Sources/eslifier/eslifier.py` and `E2E-Sources/eslifier/lib/`
- **.NET plugin record-conversion implementation:** `E2E-Sources/eslifier/backend/`
- **PyInstaller command:** `E2E-Sources/tools/build_eslifier_exe.py`
- **Tests:** `E2E-Sources/eslifier/tests/`
- **Source-package SHA-256 manifest:** `E2E-Sources/SOURCE_MANIFEST.json`
- **Dependency licence information:** `E2E-Sources/licenses/`
- **Dependency source snapshots:** `E2E-Sources/distribution-sources/`

**Packaging method:** `PyInstaller --onedir --windowed`, with the bundled Python/Tk app, a compiled framework-dependent .NET 8 backend, license files, and a matching supplied native `LELightSupport.dll`. The output is a **directory**, not just a stand-alone `.exe` file. Exact instructions: [`BUILDING.md`](BUILDING.md).

## Exclusions that are important to the review

This is a **source-only package for the E2E desktop utility**, not the entire native Skyrim LE light-plugin project. It intentionally does **not** contain:

- `LELightSupport.dll`, the SKSE runtime component required by E2E packaging;
- the runtime's C++ source code / SDK / native tests;
- compiled Windows executables, an installer, or a guaranteed bit-identical build of a specific Nexus upload.

The Python source defines the expected **runtime DLL SHA-256** as:

```text
8163276742248b229889ff071bf02c9d51cdb51e0812b0aebec313352b86a04e
```

Reviewers should obtain the runtime artifact through the corresponding separately published release and verify it independently. They may also compare their own compiled `E2E.exe` and bundle files against the exact quarantined upload (and review any differences in build toolchain and DLL versions).

## Suggested message for a Nexus Mods review request

> Hello Nexus Mods moderation team,  
> I am providing the E2E / ESLifier LE application sources, the .NET backend, third-party licence notices, a complete source manifest, and step-by-step Windows/PyInstaller build instructions for review. The tool is packaged using PyInstaller in one-folder (`--onedir`) mode. The native `LELightSupport.dll` runtime is a separate release dependency and is not included in this source repository; its required SHA-256 is documented. I understand that providing code does not itself establish that the uploaded binary is safe. Please review the submitted archive and let me know whether you need its exact SHA-256, build logs, or any additional source/binary artifacts to complete the quarantine review. Thank you.

Providing this repository **does not automatically clear a Nexus quarantine**; moderation still needs to evaluate the actual uploaded files and may need the native DLL's source/binaries as well.