"""
Acá van otras funciones que pueden ser de utilidad pero no encajaban temáticamente en ningún lado.
"""

import re

def col_to_num(letters: str) -> int:
# Convert column letters -> number
    num = 0
    for c in letters:
        num = num * 26 + (ord(c) - ord('A') + 1)
    return num

def num_to_col(num: int) -> str:
# Convert number -> column letters
    letters = ""
    while num > 0:
        num, rem = divmod(num - 1, 26)
        letters = chr(rem + ord('A')) + letters
    return letters

def get_cell_offset(cell: str, row_offset: int = 0, col_offset: int = 0) -> str:
    """
    Return a new cell address offset by the given rows and columns.
    Works for multi-letter columns!
    Example:
        get_cell_offset("H27", row_offset=1) -> "H28"
        get_cell_offset("H27", col_offset=2) -> "J27"
        get_cell_offset("H27", row_offset=2, col_offset=3) -> "K29"
    """
    # Parse the cell into column letters and row number
    match = re.match(r"([A-Z]+)([0-9]+)", cell.upper())
    if not match:
        raise ValueError(f"Invalid cell format: {cell}")
    
    col_letters, row_str = match.groups()
    row = int(row_str)

    col_num = col_to_num(col_letters)
    new_col_num = col_num + col_offset
    new_row = row + row_offset

    if new_col_num <= 0 or new_row <= 0:
        raise ValueError("Invalid offset: resulting cell is out of range")

    new_col_letters = num_to_col(new_col_num)
    return f"{new_col_letters}{new_row}"
