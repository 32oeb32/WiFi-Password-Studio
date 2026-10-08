# Architecture

## Design

The application is intentionally a single Python 3 entrypoint using only the standard library. It has three functional layers:

1. **Domain logic:** `secure_random_password`, `synthetic_word`, `memorable_password`, `custom_passphrase`, `valid_wifi_password`, `assess_password`, `patterned_candidate`.
2. **Storage:** `save_password`, `create_patterned_list`; exclusive creation (`O_EXCL`) and restrictive mode (`0600`) for local outputs.
3. **Terminal UI:** `show_banner`, `show_developer_footer`, `interactive`, input validation and error messages.

```text
User terminal
   |
   v
interactive menu
   +--> secure random / memorable / custom generator
   |           +--> WPA/WPA2 format check + optional local save
   +--> password heuristics (offline only)
   +--> synthetic dataset builder --> exclusive local file
   +--> exit
```

## Randomness

Random choices use `secrets` / `secrets.SystemRandom`, backed by the operating-system cryptographic random source. A generated password can be unpredictable when all components are selected securely; **human-chosen seed words do not inherit this property**.

## Data handling

- No external requests, telemetry, API keys or external dependencies.
- Displayed generated passwords appear in terminal output.
- The checker uses `getpass` to avoid visible input, but it does not protect process memory or swap.
- Optional exports are plaintext. Permissions are OS-dependent; safeguard files even when `0600` applies.
- The generated dataset is kept unique in memory with a `set`; generating one million entries has nontrivial memory usage.

## Known constraints

- Passphrase validation uses the WPA/WPA2-Personal 8–63 printable-ASCII rule. It does not implement every alternative network credential encoding or WPA-Enterprise policy.
- No entropy measurement or credible crack-time forecasting is provided.
- Pattern generation is random template selection, **not AI, PassGAN, PassGPT or statistical learning**.
- The program has no handshake capture, handshake verification, Wi-Fi interface manipulation, or router administration features.
- No installer/package is shipped in the source preview.

## Compatibility expectations

The initial target is Kali Linux and other Python 3-capable Linux hosts. The CI matrix exercises Ubuntu across supported Python runtimes; this is not a claim of qualified Windows or macOS operation.
