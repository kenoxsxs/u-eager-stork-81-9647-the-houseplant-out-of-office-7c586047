"""Entry program: the houseplant's out-of-office auto-reply.

One line, at most 120 characters, written as if a neglected fern sent it.
Stdlib only.
"""

import hashlib
import os
from pathlib import Path

PLANT_OOO = "Out of office. Out of water. Out of patience. The fern has left the building."


def look(line):
    """Check the line fits the bounty gate: one line, 1-120 chars, not blank."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(line) <= 120:
        raise ValueError(f"entry must be 1-120 characters, got {len(line)}")


def spot_for():
    """Resolve the output folder from the environment, defaulting to output."""
    folder = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def plant_it(target, line):
    """Write the line with exclusive creation, after clearing any stale file."""
    if target.exists():
        target.unlink()
    with open(target, "x", encoding="utf-8") as handle:
        handle.write(line)
    payload = line.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    print("planted:", target, "|", len(payload), "bytes | sha256", digest)
    return payload


def verify_plant(target, line, payload):
    """Read the file back and confirm it matches the intended bytes exactly."""
    stored = target.read_bytes()
    assert stored == payload, "written bytes differ from intended payload"
    decoded = stored.decode("utf-8")
    assert decoded == line, "decoded text differs from the entry line"
    assert decoded == decoded.strip(), "entry has trailing whitespace"
    assert "\n" not in decoded, "entry must be a single line"


def run_plant():
    """Validate, write, and verify the houseplant out-of-office line."""
    look(PLANT_OOO)
    target = spot_for()
    payload = plant_it(target, PLANT_OOO)
    verify_plant(target, PLANT_OOO, payload)


if __name__ == "__main__":
    run_plant()
