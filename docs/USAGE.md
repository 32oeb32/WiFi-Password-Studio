# Usage guide

## Start

From the repository root:

```bash
python3 wifi_password_studio_v2.py
```

The menu shows six options and an informational developer-contact footer. ANSI colors are used on supported terminals, and honor `NO_COLOR` and `TERM=dumb`.

## Option 1 — Strong random password

Choose a length between 8 and 63, with 20 as the default. Python's `secrets` module supplies randomness. The program enforces that at least one lowercase letter, uppercase letter, digit, and configured symbol appears. This composition rule is a UI choice, not a claim that symbols are essential for every secure password.

For real Wi-Fi use, prefer a long generated password and store it in a trusted password manager. The program may print it on screen; avoid terminal recording and shoulder surfing.

## Option 2 — Random memorable passphrase

Choose 4–7 synthetic pronounceable words. The default is 6. Independent random selections are joined by `-`. Generated tokens come from an internal synthetic word space; they are not personal-profile words and should not be interpreted as a curated dictionary of natural-language terms.

## Option 3 — Custom-word passphrase

Supply 3–6 comma-separated ASCII words, each 3–16 letters. The script joins title-cased words with hyphens and appends an exclamation mark plus five random digits. A familiar phrase remains guessable even if it includes symbols and numbers, so this mode is explicitly labeled **less secure**.

## Option 4 — Evaluate a password

You type an existing password without echoing it. The checker warns about short lengths, common substrings, year-like numbers, repeated runs, simple sequences, and WPA/WPA2 formatting. This is a small heuristic, **not a breach search, entropy proof or definitive rating**. The password stays local in process memory and is not transmitted.

## Option 5 — Synthetic patterned dataset

Enter comma-separated **fictional/non-sensitive** tokens, optionally opt into a small common-word set, choose 1–1,000,000 unique output entries, and give an output path. The generator uses structural templates such as separators, digits, years and case variations. These entries model human password patterns; **they should not be used as recommended new credentials**.

The program writes one entry per line to a newly created ASCII text file, attempts owner-only `0600` permissions on POSIX systems, and refuses to overwrite an existing file. Large datasets can consume memory and disk and take time to generate. Interrupted generation may leave no file or an incomplete run; do not assume an interrupted run succeeded.

Example **synthetic training seeds**: `nebula, lighthouse, 47`. Do not feed in a real person's identity, family dates or actual passwords.

## Saving credentials

For options 1–3, the application asks whether to save the generated result to a plaintext file. The default is **No**. When saved, the file is created exclusively and not silently overwritten. Always treat saved password files as secrets.

## Self-test

```bash
python3 wifi_password_studio_v2.py --self-test
python3 -m unittest discover -s tests -v
```

Tests do not require a network, root permissions or a physical Wi-Fi adapter.
