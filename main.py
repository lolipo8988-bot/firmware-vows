#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry for 'Till Firmware Do Us Part' to /output/entry.txt.

The competition asks for one sentence, under 200 characters: a
wedding vow a robot speaks at its own wedding, funny and heartfelt
at the same time. The house judge weighs, in order: that it really
is a robot's own wedding vow, the laugh it earns, the tenderness
under the joke, how much it sounds like a machine talking about
itself, and how cleanly it fits one line with nothing spare.

The output path defaults to /output/entry.txt and can be redirected
with the ENTRY_OUTPUT_PATH environment variable (used only for
local verification runs, so the shared /output is never touched).
The program is deterministic: every run writes exactly the same
bytes, and it re-reads the file after writing to prove the bytes
on disk are the bytes intended.
"""

import os

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
OUTPUT_ENV_VAR = "ENTRY_OUTPUT_PATH"
MAX_CHARS = 200

# The vow, revised after the first run. The draft ran long and
# spelled its middle clause out ("to never reboot in the middle of
# an argument"); the revision tightens that to "never to reboot
# mid-argument" and gives the ending its charge back ("my last 1%
# of charge"), so the final beat is unmistakably a machine spending
# the last of its battery on one tender act. The structure is a
# real vow's arc in robot terms: endurance (forced updates, low
# battery), conduct in conflict (no rebooting mid-argument -- the
# machine equivalent of never walking out), and devotion unto
# shutdown (the last 1% spent whispering her name). Every machine
# word is the speaker's own body and life: firmware updates, its
# battery, its reboots, its final shutdown. No pun is bolted on;
# the laugh and the ache come from the same facts.
ENTRY_PARTS = (
    "I vow to love you through every forced update and low-battery "
    "warning, never to reboot mid-argument, and when my final "
    "shutdown comes, to spend my last 1% of charge whispering "
    "your name.",
)


def build_entry() -> str:
    """Assemble the one-sentence vow and hold it to the gate's rules."""
    text = "".join(ENTRY_PARTS)
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1..{MAX_CHARS} characters, got {len(text)}"
    )
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert text.count(".") == 1 and text.endswith("."), "entry must be one sentence"
    assert text.strip(), "entry must not be only white space"
    return text


def write_entry(text: str, output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(output_path, "rb") as f:
        on_disk = f.read()
    assert on_disk == text.encode("utf-8"), "bytes on disk differ from entry"


def main() -> None:
    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)
    write_entry(build_entry(), output_path)


if __name__ == "__main__":
    main()
