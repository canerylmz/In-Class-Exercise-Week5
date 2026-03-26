"""
Programming for the Puzzled -- Srini Devadas
You Will All Conform

Given a list of cap directions represented as 'F' (forwards) and 'B' (backwards),
print the minimal set of flip commands to make all caps end up in the same direction.

The strategy is:
- Split the input into maximal contiguous runs (intervals) of equal direction.
- Flip every run of the direction that has fewer runs.

Tie-breaking: if both directions have the same number of runs, this implementation
chooses to flip the 'B' runs (to match the original script behavior).
"""

from __future__ import annotations

from collections.abc import Sequence


def _normalize_caps(caps: Sequence[str]) -> list[str]:
    """Normalize and validate cap directions.

    Args:
        caps: Sequence containing direction tokens.

    Returns:
        A list of uppercase tokens, each either 'F' or 'B'.

    Raises:
        ValueError: If any token is not one of {'F', 'B'} (case-insensitive).
    """
    normalized: list[str] = []
    for idx, token in enumerate(caps):
        if not isinstance(token, str):
            raise ValueError(
                f"Invalid cap at index {idx}: expected 'F' or 'B' as a string, "
                f"got {type(token).__name__}."
            )
        t = token.upper()
        if t not in {"F", "B"}:
            raise ValueError(
                f"Invalid cap at index {idx}: {token!r}. Expected 'F' or 'B'."
            )
        normalized.append(t)
    return normalized


def _segments(caps: Sequence[str]) -> list[tuple[int, int, str]]:
    """Split caps into maximal contiguous segments of equal values."""
    if not caps:
        return []

    segments: list[tuple[int, int, str]] = []
    start = 0
    for i in range(1, len(caps)):
        if caps[i] != caps[i - 1]:
            segments.append((start, i - 1, caps[i - 1]))
            start = i
    segments.append((start, len(caps) - 1, caps[-1]))
    return segments


def conform_commands(caps: Sequence[str]) -> list[str]:
    """Compute the minimal flip commands required for conformity.

    Args:
        caps: Sequence of cap directions ('F'/'B', case-insensitive).

    Returns:
        A list of human-readable command strings. If the input is empty, returns [].

    Raises:
        ValueError: If any element in `caps` is not 'F' or 'B'.
    """
    normalized = _normalize_caps(caps)
    if not normalized:
        return []

    segments = _segments(normalized)

    forward_runs = sum(1 for _, _, t in segments if t == "F")
    backward_runs = len(segments) - forward_runs

    # Direction whose runs we will flip to match the other direction.
    flip_dir = "F" if forward_runs < backward_runs else "B"

    commands: list[str] = []
    for start_idx, end_idx, cap_type in segments:
        if cap_type != flip_dir:
            continue

        if start_idx == end_idx:
            commands.append(f"Person in position {start_idx} flip your cap!")
        else:
            commands.append(
                f"People in positions {start_idx} through {end_idx} flip your caps!"
            )
    return commands


def please_conform(caps: Sequence[str]) -> None:
    """Print minimal flip commands to make all caps conform.

    This is a thin wrapper around `conform_commands` kept for compatibility with the
    original script.
    """
    for cmd in conform_commands(caps):
        print(cmd)


if __name__ == "__main__":
    caps_list = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"]
    caps_list_2 = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "F", "F"]

    print("Testing first caps list:")
    please_conform(caps_list)

    print("\nTesting second caps list:")
    please_conform(caps_list_2)