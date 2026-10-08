# Development guide

## Runtime

Python 3.10+ and standard library only. Keep the main file directly runnable on Kali Linux without `pip install`.

## Local checks

```bash
python3 -m py_compile wifi_password_studio_v2.py
python3 wifi_password_studio_v2.py --self-test
python3 -m unittest discover -s tests -v
printf '6\n' | NO_COLOR=1 python3 wifi_password_studio_v2.py
```

## Change control

- Keep the six-option interface stable in version 2.x.
- Keep generated outputs constrained to WPA/WPA2 printable-ASCII passphrase rules when described as WPA2-compatible.
- Do not convert the offline app into a network scanning or handshake-cracking utility.
- Avoid logging, storing or shipping real secrets and personally identifying candidate lists.
- Extend tests whenever data handling, export semantics or random password generation changes.
- Prefer targeted improvements over adding runtime dependencies or replacing the existing compact banner.

## Pull requests

Include a motivation, behavior summary, affected user options, tests executed, and any security/privacy impact. For changes in password-generation algorithms, explain whether unpredictability is materially improved or weakened. Explicitly label any synthetic demonstration, estimation or unverified claim.
