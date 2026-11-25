"""The Funniest Honest Appliance Error — make.fun entry.

Writes one line (at most 200 characters): the funniest honest error message
an appliance could show, to /output/entry.txt.

The line: a washing machine whose drain pump is blocked by a coin, in the
machine's own flat, put-upon voice. The fault is real — coins blocking the
drain pump are one of the most common causes of a washer drain error — and
the laugh comes out of the truth of it: the machine keeps the coin.

Why this line works (the joke, in one paragraph): the best honest errors
sound like a person who has had enough, not like a manual. "Error E12" is
the dry, official frame; "Drain pump blocked by a coin" is the true fault;
"I am keeping it" is the machine quietly admitting it has taken a finder's
fee; "Call an engineer" is the shrug that closes it. Four beats, 75
characters, one line, no setup the reader has to decode — the appliance is
the straight man and the punchline at once.

Structure: validate_entry() enforces the competition gate (1-200 chars, one
line, non-blank, UTF-8); write_entry() writes the validated text and
verifies it by reading it back; main() ties the two together.

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


def write_entry(text, path=OUTPUT_PATH):
    """Write the validated entry text to path, then verify it by reading it
    back: the bytes on disk must be exactly text encoded as UTF-8.

    Returns the sha256 hex digest of the bytes written, so callers can
    confirm the output is byte-identical across runs.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "rb") as f:
        raw = f.read()
    if raw != text.encode("utf-8"):
        raise ValueError("read-back mismatch: %s differs from entry text" % path)
    return hashlib.sha256(raw).hexdigest()


def main():
    validate_entry(ENTRY_TEXT)
    digest = write_entry(ENTRY_TEXT)
    print("wrote %s (%d characters, %d bytes, sha256 %s)"
          % (OUTPUT_PATH, len(ENTRY_TEXT), len(ENTRY_TEXT.encode("utf-8")), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
