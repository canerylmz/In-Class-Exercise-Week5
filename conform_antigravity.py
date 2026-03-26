"""
Programming for the Puzzled -- Srini Devadas
You Will All Conform

Input is a list of 'F's and 'B's, in terms of forwards and backwards caps.
Output is a set of commands to get either all 'F's or all 'B's.
Fewest commands are the goal.
"""

from collections.abc import Sequence


def get_conform_commands(caps: Sequence[str]) -> list[str]:
    """
    Analyzes a sequence of caps and determines the minimal set of 
    commands required to make all caps conform to the same direction.
    
    Args:
        caps: A sequence of strings representing cap directions, 
              where 'F' is forward and 'B' is backward.
              
    Returns:
        A list of command strings to be executed.
        
    Raises:
        ValueError: If the input sequence contains invalid characters.
    """
    if not caps:
        return []

    intervals: list[tuple[int, int, str]] = []
    start = 0
    prev_cap = caps[0]

    # Validate the first element
    if prev_cap not in {'F', 'B'}:
        raise ValueError(f"Invalid cap character at index 0: '{prev_cap}'. Expected 'F' or 'B'.")

    # Determine intervals where caps are in the same direction
    for i, cap in enumerate(caps):
        if cap not in {'F', 'B'}:
            raise ValueError(f"Invalid cap character at index {i}: '{cap}'. Expected 'F' or 'B'.")
            
        if cap != prev_cap:
            intervals.append((start, i - 1, prev_cap))
            start = i
            prev_cap = cap

    # Append the last interval after the loop
    intervals.append((start, len(caps) - 1, prev_cap))

    # Determine which cap direction requires fewer intervals to flip
    forward_intervals = sum(1 for _, _, c in intervals if c == 'F')
    backward_intervals = sum(1 for _, _, c in intervals if c == 'B')
    flip_target = 'F' if forward_intervals < backward_intervals else 'B'

    # Generate the commands without printing them (Pure Function)
    commands = []
    for start_idx, end_idx, cap_type in intervals:
        if cap_type == flip_target:
            if start_idx == end_idx:
                commands.append(f"Person in position {start_idx} flip your cap!")
            else:
                commands.append(f"People in positions {start_idx} through {end_idx} flip your caps!")

    return commands


def please_conform(caps: Sequence[str]) -> None:
    """
    Prints the minimal number of commands needed to make all elements 
    in the array conform to the same direction.
    """
    try:
        commands = get_conform_commands(caps)
        for command in commands:
            print(command)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    caps_list = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'B', 'F']
    caps_list_2 = ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'F', 'F']
    
    print("Testing first caps list:")
    please_conform(caps_list)
    
    # print("\nTesting second caps list:")
    # please_conform(caps_list_2)
