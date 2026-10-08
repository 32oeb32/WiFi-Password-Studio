# Security considerations and threat model

## Intended scope

Wi-Fi Password Studio helps users create new WPA/WPA2-Personal passphrases, inspect obvious weaknesses in their own passwords, and produce synthetic datasets for legitimate education and controlled testing.

## Assets

- Newly generated plaintext passwords
- Passwords provided for local assessment
- Locally exported synthetic datasets

## Trust boundaries

The tool trusts the local Python interpreter and operating system. It does not authenticate an operator, encrypt exported files, wipe memory, or establish a trusted terminal. A local adversary with screen, filesystem or process access may see plaintext secrets.

## Safeguards in the current source

- Uses `secrets`, not a deterministic random seed, for password generation.
- Checks output length and printable ASCII requirements.
- Uses `getpass` to hide assessed password input in normal terminals.
- Tries to create output files atomically and refuses existing-file overwrites; uses mode `0600` on POSIX systems.
- Makes no network calls, so credentials are not uploaded by design.

## What it does not provide

- No guarantee a custom-word password is resistant to targeted guessing.
- No breach corpus query, dictionary-score calibration or entropy guarantee.
- No secure secret storage, encrypted export, or password manager integration.
- No protection if host OS, terminal, or Python runtime is compromised.
- No Wi-Fi intrusion, packet injection, credential capture or handshake-processing capability.

## Safe usage

Prefer random outputs from options 1–2 for a real router. Treat option 5 output as synthetic training data, not as high-quality secret passwords. Never upload real passwords, actual user profiles or private data in bug reports, Git commits, screenshots or test fixtures.

For a suspected vulnerability, use the private reporting channel described in the repository-level [SECURITY.md](../SECURITY.md).
