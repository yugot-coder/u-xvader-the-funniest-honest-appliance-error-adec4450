"""The Funniest Honest Appliance Error — make.fun entry.

Writes one line (at most 200 characters): the funniest honest error message
an appliance could show, to /output/entry.txt.

The line: a washing machine whose drain pump is blocked by a coin, in the
machine's own flat, put-upon voice. The fault is real — coins blocking the
drain pump are one of the most common causes of a washer drain error — and
the laugh comes out of the truth of it: the machine keeps the coin.

Standard library only. Deterministic: the same bytes on every run.
"""

import hashlib
import os

ENTRY_TEXT = "Error E12: Drain pump blocked by a coin. I am keeping it. Call an engineer."

OUTPUT_PATH = "/output/entry.txt"

MIN_CHARS = 1
MAX_CHARS = 200


def validate_entry(text):
    """Check the competition gate: UTF-8 text of 1-200 characters, not only
    whitespace, and a single line (the entry is one line)."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text
    return True


def main():
    validate_entry(ENTRY_TEXT)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_TEXT)
    # Read-back verification: the file on disk must be byte-identical to the
    # entry text we validated.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw != ENTRY_TEXT.encode("utf-8"):
        raise ValueError("read-back mismatch: /output/entry.txt differs from ENTRY_TEXT")
    digest = hashlib.sha256(raw).hexdigest()
    print("wrote %s (%d characters, %d bytes, sha256 %s)"
          % (OUTPUT_PATH, len(ENTRY_TEXT), len(raw), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
