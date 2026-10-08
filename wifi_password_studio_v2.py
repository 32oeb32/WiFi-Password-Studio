#!/usr/bin/env python3
"""Wi-Fi Password Studio — offline password creation and basic auditing.

Standard-library only. Intended for passwords you own or are creating.
"""

from __future__ import annotations

import argparse
import getpass
import os
from pathlib import Path
import re
import shutil
import sys
import secrets
import string

APP_NAME = "Wi-Fi Password Studio"
SYMBOLS = "!@#$%^&*_-+=?"
LETTERS = string.ascii_letters
DIGITS = string.digits
ALPHABET = LETTERS + DIGITS + SYMBOLS

# 32 x 16 x 32 = 16,384 possible synthetic words (14 bits per word).
START = (
    "bal", "bel", "bir", "bor", "cal", "cel", "cir", "cor",
    "dal", "del", "dir", "dor", "fal", "fel", "fir", "for",
    "gal", "gel", "gir", "gor", "kal", "kel", "kir", "kor",
    "mal", "mel", "mir", "mor", "sal", "sel", "sir", "sor",
)
MIDDLE = (
    "a", "e", "i", "o", "u", "ae", "ai", "ea",
    "io", "oa", "ou", "ei", "ia", "ue", "y", "oo",
)
END = (
    "ban", "ben", "bin", "bon", "dan", "den", "din", "don",
    "far", "fer", "fir", "for", "gan", "gen", "gin", "gon",
    "lan", "len", "lin", "lon", "mar", "mer", "mir", "mor",
    "nar", "ner", "nir", "nor", "ran", "ren", "rin", "ron",
)
COMMON = ("password", "admin", "welcome", "qwerty", "letmein", "123456", "iloveyou")


def valid_wifi_password(password: str) -> bool:
    """WPA/WPA2-Personal passphrase: 8..63 printable ASCII characters."""
    return 8 <= len(password) <= 63 and all(32 <= ord(c) <= 126 for c in password)


def secure_random_password(length: int = 20) -> str:
    if not 8 <= length <= 63:
        raise ValueError("Choose a length between 8 and 63 characters.")
    # Enforce presence of lower, upper, digits, symbols; shuffle securely.
    while True:
        password = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in SYMBOLS for c in password)):
            return password


def synthetic_word() -> str:
    return secrets.choice(START) + secrets.choice(MIDDLE) + secrets.choice(END)


def memorable_password(word_count: int = 6, separator: str = "-") -> str:
    if not 4 <= word_count <= 7:
        raise ValueError("Choose 4–7 words.")
    if separator not in ("-", ".", "_", "!"):
        raise ValueError("Invalid separator.")
    # Six independent selections provide 84 bits of nominal search entropy.
    password = separator.join(synthetic_word() for _ in range(word_count))
    if not valid_wifi_password(password):
        raise ValueError("Result exceeds the WPA2 length limit; use fewer words.")
    return password


def custom_passphrase(words: str) -> str:
    """Create a memorable phrase; user-chosen words are NOT random entropy."""
    cleaned = [w.strip() for w in words.split(",") if w.strip()]
    if not 3 <= len(cleaned) <= 6:
        raise ValueError("Enter 3–6 comma-separated words.")
    if any(not re.fullmatch(r"[A-Za-z]{3,16}", w) for w in cleaned):
        raise ValueError("Use ASCII letters only (3–16 per word).")
    # One finished password, not a targeted candidate-list generator.
    password = "-".join(w.title() for w in cleaned)
    password += "!" + str(secrets.randbelow(90000) + 10000)
    if not valid_wifi_password(password):
        raise ValueError("Phrase too long for WPA2. Use shorter words.")
    return password


def assess_password(password: str) -> list[str]:
    warnings = []
    if not valid_wifi_password(password):
        warnings.append("Not a valid WPA/WPA2 passphrase (8–63 printable ASCII characters).")
    if len(password) < 16:
        warnings.append("Consider at least 16–20 randomly generated characters.")
    lower = password.lower()
    if any(word in lower for word in COMMON):
        warnings.append("Contains a widely used password word or sequence.")
    if re.search(r"(?:19|20)\d\d", password):
        warnings.append("Contains a year-like number; avoid personal dates.")
    if re.search(r"(.)\1{3,}", password):
        warnings.append("Contains a long repeated-character sequence.")
    if re.search(r"(?:abcd|qwer|1234|4321)", lower):
        warnings.append("Contains a predictable keyboard/alphabet/number sequence.")
    if not any(c in SYMBOLS for c in password):
        warnings.append("No symbols; not a problem for sufficiently random long passwords.")
    if not warnings:
        warnings.append("No basic weaknesses detected. This is not a security guarantee.")
    return warnings


# Optional, generic words used in many human-created passwords.
# Never inserted unless the operator explicitly opts in.
POPULAR_SEEDS = ("password", "welcome", "hello", "admin", "love", "home", "wifi")
LEET_MAP = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}
LIST_SYMBOLS = "!@#$%&*_-+.?"


def parse_seed_words(raw: str, include_popular: bool = False) -> list[str]:
    """Read only explicitly supplied ASCII tokens, optionally generic words."""
    tokens = [item.strip() for item in raw.split(",")]
    if any(item and (len(item) > 32 or not all(33 <= ord(c) <= 126 for c in item))
           for item in tokens):
        raise ValueError("Each seed must be 1–32 printable ASCII characters, without spaces.")
    words = list(dict.fromkeys(item for item in tokens if item))
    if include_popular:
        words = list(dict.fromkeys(words + list(POPULAR_SEEDS)))
    if not words:
        raise ValueError("Enter at least one seed word.")
    return words


def word_variant(word: str, rng: secrets.SystemRandom) -> str:
    """Select one of several familiar case and substitution patterns."""
    style = rng.randrange(6)
    if style == 0:
        return word.lower()
    if style == 1:
        return word.title()
    if style == 2:
        return word.upper()
    if style == 3:
        return word.swapcase()
    if style == 4:
        return word
    # Common leet substitutions; do not add unrelated dictionary words.
    transformed = "".join(
        LEET_MAP.get(ch.lower(), ch) if rng.randrange(3) == 0 else ch
        for ch in word.title()
    )
    return transformed


def patterned_candidate(words: list[str], rng: secrets.SystemRandom) -> str:
    """Create candidates from generic human-style templates, not a handshake."""
    first = word_variant(rng.choice(words), rng)
    second = word_variant(rng.choice(words), rng)
    sym = rng.choice(LIST_SYMBOLS)
    digits = str(rng.randrange(0, 10 ** rng.choice((2, 3, 4, 5, 6)))).zfill(rng.choice((2, 3, 4)))
    year = str(rng.randrange(1970, 2041))
    sep = rng.choice("._-!@")
    templates = (
        lambda: first + digits,
        lambda: first + digits + sym,
        lambda: first + sym + digits,
        lambda: sym + first + digits,
        lambda: digits + first + sym,
        lambda: first + year,
        lambda: first + year + sym,
        lambda: first + sep + year,
        lambda: first + second + digits,
        lambda: first + sep + second + digits,
        lambda: first + sym + second + sym + digits,
        lambda: first + digits + second,
        lambda: first + second + sym,
        lambda: first + sep + second + sym,
        lambda: first + sym + digits + sym + second,
    )
    return rng.choice(templates)()


def create_patterned_list(
    words: list[str],
    amount: int,
    path: Path,
    *,
    progress: bool = False,
) -> int:
    """Write unique WPA2-compatible entries, one per line, with no overwrites."""
    if not 1 <= amount <= 1_000_000:
        raise ValueError("Choose 1–1,000,000 candidates.")
    if not words:
        raise ValueError("Enter at least one seed word.")

    path = path.expanduser()
    rng = secrets.SystemRandom()
    seen: set[str] = set()
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="ascii", buffering=1024 * 1024) as output:
            attempts = 0
            # All patterns have wide digit and symbol ranges, including with one seed.
            # Fail explicitly rather than silently hang in the event of too many collisions.
            max_attempts = max(10_000, amount * 100)
            while len(seen) < amount:
                attempts += 1
                if attempts > max_attempts:
                    raise RuntimeError("Unable to produce more unique candidates with these seeds.")
                candidate = patterned_candidate(words, rng)
                if not valid_wifi_password(candidate) or candidate in seen:
                    continue
                seen.add(candidate)
                output.write(candidate + "\n")
                if progress and len(seen) % 100_000 == 0:
                    print(f"  Generated: {len(seen):,}/{amount:,}")
    except BaseException:
        # Never leave a partial list that appears complete.
        path.unlink(missing_ok=True)
        raise
    return len(seen)


def list_builder() -> None:
    print("\nHuman-pattern candidate list builder")
    print("Uses only your input, unless you enable generic popular words.")
    raw = input("Seed words/numbers (comma-separated): ")
    extra = input("Add generic words (password, welcome, wifi, etc.)? [y/N]: ")
    words = parse_seed_words(raw, extra.strip().lower() == "y")
    amount = ask_int("Number of unique entries (1–1000000)", 1000, 1, 1_000_000)
    destination = input("Output file [patterned_candidates.txt]: ").strip() or "patterned_candidates.txt"
    path = Path(destination).expanduser()
    print(f"Creating {amount:,} entries from {len(words)} seed(s)...")
    total = create_patterned_list(words, amount, path, progress=True)
    print(f"Created {total:,} unique WPA/WPA2-compatible entries: {path.resolve()}")
    print("File permissions: owner read/write only (0600).")
    print("Note: this list is for an authorized security lab, not a secure password source.")


def ask_int(prompt: str, default: int, minimum: int, maximum: int) -> int:
    raw = input(f"{prompt} [{default}]: ").strip()
    try:
        value = int(raw) if raw else default
    except ValueError as exc:
        raise ValueError("Please enter a whole number.") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"Choose a value from {minimum} to {maximum}.")
    return value


def save_password(password: str) -> None:
    if input("Save to a private text file? [y/N]: ").strip().lower() != "y":
        return
    raw_path = input("File path [wifi_password.txt]: ").strip() or "wifi_password.txt"
    path = Path(raw_path).expanduser()
    # Fail rather than overwrite or follow an existing symlink.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="ascii") as f:
        f.write(password + "\n")
    print(f"Saved securely (owner-only permissions): {path.resolve()}")
    print("Keep this file private; plaintext passwords can be read by anyone with access.")


def show_generated(password: str) -> None:
    print("\nGenerated password:\n" + password)
    print(f"Length: {len(password)} | WPA/WPA2: {'valid' if valid_wifi_password(password) else 'invalid'}")
    save_password(password)


def terminal_colors() -> bool:
    return (sys.stdout.isatty() and "NO_COLOR" not in os.environ
            and os.getenv("TERM") != "dumb")


def colored(text: str, code: str) -> str:
    return f"\x1b[{code}m{text}\x1b[0m" if terminal_colors() else text


def show_banner() -> None:
    """Compact, regular monospace lettering — no oversized ASCII font."""
    width = shutil.get_terminal_size((80, 24)).columns
    frame = min(56, max(0, width - 2))
    print()
    print(colored("─" * frame, "2;36"))
    print("  " + colored("SPES_MEA_IN_DEO_EST#32", "1;36"))
    print("  " + colored("#DEV32#", "1;32"))
    print(colored("─" * frame, "2;36"))
    print("  " + colored(APP_NAME, "1;37") + colored("  ·  Offline password lab", "2;37"))


def show_developer_footer() -> None:
    """Short footer, no decorative block letters or oversized box."""
    width = shutil.get_terminal_size((80, 24)).columns
    frame = min(56, max(0, width - 2))
    print("\n" + colored("─" * frame, "2;36"))
    print(colored("DEV32", "1;32") + "  ·  Ideas or feedback? Get in touch.")
    print("Optional donations help keep development going.")
    print(colored("dev32@apex32-secure.com", "1;36"))


def interactive() -> None:
    show_banner()
    while True:
        print("\n1) Strong random Wi-Fi password")
        print("2) Random memorable passphrase")
        print("3) Custom-word passphrase (less secure)")
        print("4) Evaluate an existing password")
        print("5) Build patterned candidate wordlist")
        print("6) Exit")
        show_developer_footer()
        try:
            selection = input("\nChoose [1-6]: ").strip()
            if selection == "1":
                length = ask_int("Characters", 20, 8, 63)
                show_generated(secure_random_password(length))
            elif selection == "2":
                count = ask_int("Number of random words", 6, 4, 7)
                show_generated(memorable_password(count))
            elif selection == "3":
                print("Use fictional or nonpersonal words; familiar words are easier to guess.")
                words = input("Enter 3–6 words separated by commas: ")
                show_generated(custom_passphrase(words))
            elif selection == "4":
                password = getpass.getpass("Password to assess (hidden): ")
                print("\nBasic assessment:")
                for note in assess_password(password):
                    print(" - " + note)
                print("This check does not test leaked-password databases or real crack resistance.")
            elif selection == "5":
                list_builder()
            elif selection == "6":
                print("Goodbye.")
                break
            else:
                print("Choose 1, 2, 3, 4, 5, or 6.")
        except (ValueError, FileExistsError, PermissionError, OSError) as exc:
            print(f"Error: {exc}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break


def self_test() -> None:
    for n in (8, 20, 63):
        for _ in range(25):
            p = secure_random_password(n)
            assert valid_wifi_password(p) and len(p) == n
    for n in (4, 5, 6, 7):
        p = memorable_password(n)
        assert valid_wifi_password(p)
    assert valid_wifi_password(custom_passphrase("lighthouse, maple, sky"))
    assert not valid_wifi_password("short")
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as folder:
        path = Path(folder) / "test_candidates.txt"
        seeds = parse_seed_words("nebula, orbit, 32")
        assert create_patterned_list(seeds, 1000, path) == 1000
        candidates = path.read_text().splitlines()
        assert len(candidates) == len(set(candidates)) == 1000
        assert all(valid_wifi_password(s) for s in candidates)
        assert (path.stat().st_mode & 0o777) == 0o600
    assert assess_password("password123!")
    print("Self-test passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--self-test", action="store_true", help="Run built-in checks")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        interactive()
