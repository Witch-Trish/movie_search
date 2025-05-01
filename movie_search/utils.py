import os

def center_text(text, console_width=80):
    """Center text or multi-line text (e.g., tabulate tables) in the console."""
    try:
        console_width = os.get_terminal_size().columns
    except OSError:
        console_width = 80  # Fallback width if console size detection fails

    centered_lines = []
    for line in text.splitlines():
        # Remove trailing whitespace and center the line
        line = line.rstrip()
        padding = (console_width - len(line)) // 2
        centered_line = ' ' * padding + line
        centered_lines.append(centered_line)
    return '\n'.join(centered_lines)