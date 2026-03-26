"""Utilities for solving the classic "You Will All Conform" cap-flipping puzzle.

The module accepts a sequence of cap directions and computes the minimum number
of flip commands needed to make everyone face the same way. The public API keeps
`please_conform` for compatibility with the original script while exposing pure
helper functions that are easier to test and reuse.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

VALID_CAP_DIRECTIONS = frozenset({"F", "B"})


@dataclass(frozen=True, slots=True)
class CapInterval:
    """Represents a contiguous interval of identical cap directions.

    Attributes:
        start: Zero-based start index of the interval.
        end: Zero-based end index of the interval.
        direction: Cap direction stored in normalized form as ``"F"`` or ``"B"``.
    """

    start: int
    end: int
    direction: str


def normalize_caps(caps: Sequence[str]) -> list[str]:
    """Validate and normalize cap directions.

    Args:
        caps: Sequence of cap directions. Values must be strings equal to
            ``"F"`` or ``"B"`` in any letter case.

    Returns:
        A new list containing uppercase cap directions.

    Raises:
        TypeError: If ``caps`` is not a sequence or contains non-string values.
        ValueError: If any cap direction is not ``"F"`` or ``"B"``.
    """

    if isinstance(caps, (str, bytes)) or not isinstance(caps, Sequence):
        raise TypeError("caps must be a sequence of 'F'/'B' strings.")

    normalized_caps: list[str] = []
    for index, cap in enumerate(caps):
        if not isinstance(cap, str):
            raise TypeError(
                f"Cap at index {index} must be a string, got {type(cap).__name__}."
            )

        normalized_cap = cap.strip().upper()
        if normalized_cap not in VALID_CAP_DIRECTIONS:
            raise ValueError(
                f"Invalid cap direction at index {index}: {cap!r}. "
                "Expected 'F' or 'B'."
            )

        normalized_caps.append(normalized_cap)

    return normalized_caps


def build_intervals(caps: Sequence[str]) -> list[CapInterval]:
    """Group adjacent equal cap directions into intervals.

    Args:
        caps: Validated sequence of normalized cap directions.

    Returns:
        A list of contiguous intervals. Returns an empty list for empty input.
    """

    if not caps:
        return []

    intervals: list[CapInterval] = []
    start_index = 0

    for index in range(1, len(caps)):
        if caps[index] != caps[index - 1]:
            intervals.append(
                CapInterval(
                    start=start_index,
                    end=index - 1,
                    direction=caps[index - 1],
                )
            )
            start_index = index

    intervals.append(
        CapInterval(
            start=start_index,
            end=len(caps) - 1,
            direction=caps[-1],
        )
    )
    return intervals


def choose_flip_direction(intervals: Sequence[CapInterval]) -> str:
    """Choose which direction should be flipped for the minimum command count.

    Args:
        intervals: Contiguous cap intervals.

    Returns:
        ``"F"`` or ``"B"``. If both directions appear the same number of times,
        the function flips ``"B"`` intervals to preserve the original behavior.

    Raises:
        ValueError: If an interval contains an invalid direction.
    """

    forward_runs = 0
    backward_runs = 0

    for interval in intervals:
        if interval.direction == "F":
            forward_runs += 1
        elif interval.direction == "B":
            backward_runs += 1
        else:
            raise ValueError(
                f"Unsupported cap direction in interval: {interval.direction!r}"
            )

    return "F" if forward_runs < backward_runs else "B"


def generate_flip_commands(
    intervals: Sequence[CapInterval],
    flip_direction: str,
) -> list[str]:
    """Generate human-readable commands for intervals that should be flipped.

    Args:
        intervals: Contiguous cap intervals.
        flip_direction: The cap direction to flip.

    Returns:
        Command strings that can be printed directly.

    Raises:
        ValueError: If ``flip_direction`` is not ``"F"`` or ``"B"``.
    """

    if flip_direction not in VALID_CAP_DIRECTIONS:
        raise ValueError("flip_direction must be 'F' or 'B'.")

    commands: list[str] = []
    for interval in intervals:
        if interval.direction != flip_direction:
            continue

        if interval.start == interval.end:
            commands.append(f"Person in position {interval.start} flip your cap!")
        else:
            commands.append(
                f"People in positions {interval.start} through {interval.end} flip your caps!"
            )

    return commands


def conform_commands(caps: Sequence[str]) -> list[str]:
    """Compute the minimum flip commands needed to make all caps conform.

    Args:
        caps: Sequence of cap directions.

    Returns:
        A list of flip commands. Returns an empty list if ``caps`` is empty.

    Raises:
        TypeError: If the input is not a valid sequence of strings.
        ValueError: If any element is not ``"F"`` or ``"B"``.
    """

    normalized_caps = normalize_caps(caps)
    intervals = build_intervals(normalized_caps)
    if not intervals:
        return []

    flip_direction = choose_flip_direction(intervals)
    return generate_flip_commands(intervals, flip_direction)


def please_conform(caps: Sequence[str]) -> None:
    """Print the minimum flip commands needed to make all caps conform.

    Args:
        caps: Sequence of cap directions.

    Raises:
        TypeError: If the input is not a valid sequence of strings.
        ValueError: If any element is not ``"F"`` or ``"B"``.
    """

    for command in conform_commands(caps):
        print(command)


if __name__ == "__main__":
    sample_caps = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"]
    sample_caps_2 = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "F", "F"]

    print("Testing first caps list:")
    please_conform(sample_caps)

    print("\nTesting second caps list:")
    please_conform(sample_caps_2)
