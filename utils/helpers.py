from typing import List
def calculate_eta(total_weight: float) -> float:

    return total_weight


def format_path_display(path_names: List[str]) -> str:

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

    return f"ETA: {total_weight:.1f} min"


def format_dropdown_item(node_letter: str, node_name: str) -> str:

    return f"{node_letter} - {node_name}"


def parse_dropdown_selection(dropdown_text: str) -> str:

    try:
        # Split by " - " and take first part
        letter = dropdown_text.split(" - ")[0]
        return letter
    except (IndexError, ValueError) as e:
        raise ValueError(f"Invalid dropdown selection format: {dropdown_text}") from e