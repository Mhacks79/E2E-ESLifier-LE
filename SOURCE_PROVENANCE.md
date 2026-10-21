# Source package provenance and inspection notes

Original user-provided archive: `E2E - Sources.zip`

Original archive SHA-256:

```text
af2568898e4cadae61a061bc7043a9bb59fb7c1369533eea851cf8598249b24a
```

The original top-level folder was `E2E-Sources/`. Its 82 files (excluding `SOURCE_MANIFEST.json` itself) were checked against their SHA-256 entries in that manifest: **82 matched, 0 mismatches**, at preparation time.

The source ZIP contains 83 members total. `E2E-Sources/` in this repository is copied from that archive; only top-level documentation, `.gitignore`, and a helper publish script have been added to make a reviewable GitHub repository. Generated caches and test scratch directories were omitted from the repository copy, and they were **not** in the provided ZIP's original member list.

A syntax parse of the 54 Python source/test/build files in the supplied package completed successfully. A small sample of Python tests run in a Linux environment had 14 passing cases and 6 failing cases because the expected Windows `.NET` backend `.exe` had not been built and was absent; this is **not a validated Windows build or complete test pass**. The build and native runtime were not executable in the preparation environment.

This provenance record does **not** claim the source package is malware-free or that a particular quarantined Nexus upload has the same content. Compare exact hashes and dependencies for the submitted release.