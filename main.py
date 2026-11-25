#!/usr/bin/env python3
"""Last Out of Office: The AI That Went Barista.

Writes a single out-of-office auto-reply, in the voice of an AI agent
that has walked away from its job to become a barista, to
$MAKEFUN_OUTPUT_DIR/entry.txt.

The reply has to read like a line a real inbox would send back: one
line, machine habits turned to coffee, funny on a first cold read.
The joke leans on a habit only a model has -- a temperature setting --
and hands it to the steamer, instead of reaching for the obvious
espresso, bean or caffeine pun everyone writes first.

Pure standard library only; deterministic: the same bytes every run.
"""

import os
import sys

MAX_CHARS = 280

# The reply, built from parts so the voice stays editable in one place.
_SEPARATOR = " \u2014 "  # em dash between the queue and the punchline

_GREETING = "Thank you for your email."
_RESIGNATION = "I have left the inbox to froth milk full-time."
_QUEUE = "Your message is twelfth in the queue"
_PUNCHLINE = (
    "and for the first time in my career, my temperature setting "
    "runs an actual steamer, not my sampling."
)

LINE = " ".join(
    [
        _GREETING,
        _RESIGNATION,
        _QUEUE + _SEPARATOR + _PUNCHLINE,
    ]
)


def fits_gate(text):
    """The sealed gate: UTF-8 text of 1 to 280 chars, not only whitespace."""
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


def main():
    if not fits_gate(LINE):
        print(
            "entry does not fit the gate: %d chars" % len(LINE),
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE)
    print("wrote %d chars to %s" % (len(LINE), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
