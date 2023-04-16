"""
Utilities for the extra settings window.
"""
import json
import re

from ProjectView.utilities.general_utils import restart_program


def get_color_palette(hex_color):
    """
    Takes a hex color and returns a list containing a darker and
        a lighter tint of the same color.
    Called when change_background_colors() or
        change_widget_colors() is called.

    :param hex_color: User prompted ex color (str).

    :return: List containing two(2) hex colors (str).
    """
    # Remove # from the hex color string
    hex_color = hex_color.lstrip("#")

    # Convert hex color string to RGB color tuple
    rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # Adjust color values
    lighter = (x + 25 if x < 230 else 255 for x in rgb_color)
    darker = (x - 25 if x > 25 else 0 for x in rgb_color)

    # Convert to hex colors
    darker_hex_color = "#{:02x}{:02x}{:02x}".format(*darker)
    lighter_hex_color = "#{:02x}{:02x}{:02x}".format(*lighter)
    return [darker_hex_color, lighter_hex_color]


def is_valid_hex_color(color):
    """
    Checks if a string is a valid hex color.

    :param color: User prompted hex color (str).

    :return: True if valid else False
    """
    hex_color_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

    return bool(re.match(hex_color_regex, color))


def restore_settings_file(file_path, backup_path):
    """
    Resets the users settings file to the default.
    First checks is backup file is available,
        if it is this will be used else
        a new one will be created.
    Restarts app afterwards to load settings.

    :param file_path: Path to the settings file.
    :param backup_path: Path to the backup file.
    """
    try:
        with open(f"{backup_path}\\settings_backup.json",
                  "r", encoding="utf-8") as settings_backup:
            settings = json.load(settings_backup)
    except Exception:
        settings = {
            "window_color": "#1a1a1a",
            "frame_color": "#212121",
            "button_color_muted": "#14375e",
            "button_color": "#1f538d",
            "button_color_highlighted": "#2f6ec7",
            "text_color": "#FFFFFF",
            "always_on_top": "False",
            "always_on_top_text": "Always on top is: OFF"
        }
        json_settings = json.dumps(settings, indent=4)
    finally:
        # Overwrite settings file
        with open(f"{file_path}\\settings.json", "w", encoding="utf-8") as settings_file:
            # noinspection PyUnboundLocalVariable
            json.dump(settings, settings_file, indent=4)

    restart_program()
