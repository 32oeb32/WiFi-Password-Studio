# Wi-Fi Password Studio

**An offline, dependency-free Python CLI for creating and evaluating Wi-Fi passphrases and experimenting with synthetic password construction patterns.**

**Project:** APEX32 Secure · Developer Projects  
**Edition:** v2 · community preview  
**Platform:** Kali Linux and other Linux distributions with Python 3  
**Developer contact:** [dev32@apex32-secure.com](mailto:dev32@apex32-secure.com)

> **Release status:** v2 source preview. Automated checks are provided; broad-platform qualification, third-party security review, and a published GitHub release are **not yet claimed**.

```text
──────────────────────────────────────────
  SPES_MEA_IN_DEO_EST#32
  #DEV32#
──────────────────────────────────────────
  Wi-Fi Password Studio · Offline password lab
```

Wi-Fi Password Studio is a local terminal application built with Python's standard library. It performs **no network requests**, does **not connect to a router**, and does **not capture or verify Wi-Fi handshakes**. Its security assessment is a **basic heuristic check**, not a statistical crack-time estimate or breach lookup.

## Capabilities

| Menu | Capability | Key boundaries |
| --- | --- | --- |
| 1 | Strong random Wi-Fi password | CSPRNG-backed, 8–63 printable ASCII characters |
| 2 | Random memorable passphrase | Synthetic pronounceable words, configurable count |
| 3 | Custom-word passphrase | Readable but not equivalent to randomly generated secrets |
| 4 | Assess an existing passphrase | Basic local heuristics; does not check breach data |
| 5 | Build patterned candidate wordlist | 1–1,000,000 unique entries for **authorized, synthetic training data**; not a secure-password generator |
| 6 | Exit | Ends the interactive session |

## Requirements

- Python **3.10+** (standard library only; no `pip` or `sudo` required).
- A local terminal (Kali Linux recommended).
- Disk space for generated datasets and any optional plaintext password files.

## Quick start

```bash
git clone https://github.com/32oeb32/WiFi-Password-Studio.git
cd WiFi-Password-Studio
python3 wifi_password_studio_v2.py
```

If you downloaded the standalone script rather than cloning the repository, run it directly with `python3 wifi_password_studio_v2.py`.

To run internal checks:

```bash
python3 wifi_password_studio_v2.py --self-test
python3 -m unittest discover -s tests -v
```

To see CLI flags:

```bash
python3 wifi_password_studio_v2.py --help
```

## Responsible operation

- Use options 1–3 to create **new** passphrases; prefer **option 1 or 2** for actual Wi-Fi security.
- Option 5 models human-style formatting in **synthetic data**; its output should **not** be used as a new Wi-Fi password.
- Do not enter real passwords as seed data. Use the checker locally only for secrets you control.
- If exporting, output files contain **plaintext** secrets or candidate strings. Protect, relocate, and delete them appropriately. Files are created with owner-only permissions where supported, but that is not a substitute for encrypted storage.
- Outputs and strength results are **not security guarantees**. WPA/WPA2-Personal passphrases are 8–63 printable ASCII characters; other Wi-Fi authentication modes have different requirements.

## Documentation

| Document | Covers |
| --- | --- |
| [Documentation index](docs/INDEX.md) | Full reference navigation |
| [Usage guide](docs/USAGE.md) | Interactive menus, safe examples, file output |
| [Architecture](docs/ARCHITECTURE.md) | Modules, randomness, data flow, limits |
| [Security notes](docs/SECURITY.md) | Threat model, security expectations, limitations |
| [Development](docs/DEVELOPMENT.md) | Tests, review, conventions |
| [Release checklist](docs/RELEASE.md) | Qualification, tags, artifacts and publication |
| [Website integration](website/README.md) | Developer Projects card and page content |

See also [Changelog](CHANGELOG.md), [Contributing](CONTRIBUTING.md) and [Security policy](SECURITY.md).

## Roadmap

- Improve password-quality feedback with clearly labeled estimates and offline-only indicators.
- Add reproducible synthetic-data fixtures for pattern-analysis research.
- Expand automated edge-case coverage and release verification.
- Introduce stable version metadata when the release process is established.

## License and release policy

**A license has not yet been selected.** Do not represent this project as MIT/GPL/open source until the owner chooses a license and adds its terms. In the meantime, standard copyright rules apply. See [docs/RELEASE.md](docs/RELEASE.md) before publication.

---

**SPES_MEA_IN_DEO_EST#32 · #DEV32#**  
Ideas, bug reports, or feedback: **dev32@apex32-secure.com**. Optional contributions may help maintain future versions; no donation mechanism or promise of financial support is implied.
