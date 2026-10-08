# Contributing

Thank you for your interest in Wi-Fi Password Studio.

1. Check for an existing GitHub issue before creating a new one.
2. Open an issue describing the proposed change before a major refactor.
3. Keep changes compatible with Python 3.10+ without additional runtime dependencies.
4. Write tests using fictional, synthetic input only; never commit passwords used by real people or organizations.
5. Run `python3 wifi_password_studio_v2.py --self-test` and `python3 -m unittest discover -s tests -v`.
6. Explain limitations and safety tradeoffs in the pull request description.

Please do not submit changes that silently upload secret data, import unreviewed password dumps, or expand the tool into an active Wi-Fi attack suite. Security reports belong at **dev32@apex32-secure.com**.

The project owner will define licensing and code-acceptance terms before public contributions are accepted.
