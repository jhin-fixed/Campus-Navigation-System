"""
Helper utility functions for Campus Navigator.
Formatting and calculation functions.
"""

from typing import List


def calculate_eta(total_weight: float) -> float:
    """
    Calculate estimated time of arrival.
    Since weights are already in time units (minutes), just return the weight.

    Args:
        total_weight: Total path weight (time in minutes)

    Returns:
        Time in minutes (same as input)
    """
    return total_weight


def format_path_display(path_names: List[str]) -> str:
    """
    Format building names into display string.
    Format: "START: X | VIA: Y, Z | END: W"

    Args:
        path_names: Ordered list of building names along the path

    Returns:
        Formatted string for display
    """
    if len(path_names) < 2:
        return "Invalid path"

    # Direct connection (no intermediate nodes)
    if len(path_names) == 2:
        return f"START: {path_names[0]} | END: {path_names[-1]}"

    # Path with intermediate nodes
    start = path_names[0]
    end = path_names[-1]
    via = ", ".join(path_names[1:-1])

    return f"START: {start} | VIA: {via} | END: {end}"


def format_eta_display(total_weight: float) -> str:
    """
    Format ETA for display.
    Since we're using time-based weights, just show the time.

    Args:
        total_weight: Total path weight (time in minutes)

    Returns:
        Formatted string like "ETA: 8.5 min"
    """
    return f"ETA: {total_weight:.1f} min"


def format_dropdown_item(node_id: int, node_name: str) -> str:
    """
    Format a node for dropdown display.
    Format: "ID - Name" (e.g., "0 - Entrance")

    Args:
        node_id: Node ID
        node_name: Node name

    Returns:
        Formatted string for dropdown
    """
    return f"{node_id} - {node_name}"


def parse_dropdown_selection(dropdown_text: str) -> int:
    """
    Extract node ID from dropdown selection text.

    Args:
        dropdown_text: Text in format "ID - Name"

    Returns:
        Node ID as integer

    Raises:
        ValueError: If text format is invalid
    """
    try:
        # Split by " - " and take first part
        id_str = dropdown_text.split(" - ")[0]
        return int(id_str)
    except (IndexError, ValueError) as e:
        raise ValueError(f"Invalid dropdown selection format: {dropdown_text}") from e