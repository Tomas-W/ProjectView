"""
General use utilities.
"""
import json
import os
import sys

APPLICATION_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
APP_SETTINGS_FOLDER = os.path.join(APPLICATION_DIR, "ProjectView\\app_settings")
APP_SETTINGS_BACKUP_FOLDER = os.path.join(APPLICATION_DIR, "ProjectView\\app_settings\\backups")


def get_user_setting(setting):
    """
    Reads settings file and returns the settings value.

    :param setting: Name of the setting to get value of (str).

    :return: Value of the setting (str).
    """
    with open(f"{APP_SETTINGS_FOLDER}\\settings.json", "r", encoding="utf-8") as settings_file:
        settings_data = json.load(settings_file)
        setting_value = settings_data[setting]

    return setting_value


def set_user_settings(settings, values):
    """
    Reads settings file and overwrites the keys values passed in.

    :param settings: List of names of settings to overwrite the value of (list).
    :param values: List of names of values to be overwritten (list).
    """
    with open(f"{APP_SETTINGS_FOLDER}\\settings.json", "r+", encoding="utf-8") as settings_file:
        user_settings = json.load(settings_file)

        for setting, value in zip(settings, values):
            user_settings[setting] = value

        settings_file.seek(0)
        json.dump(user_settings, settings_file, indent=4)


def get_color_settings():
    """
    Reads settings file and returns a dictionary
        containing the color names and values in hex.
    Called before app is created and when extra settings window is opened.

    :return: Dictionary containing the color names and values in hex (dict).
    """
    with open(f"{APP_SETTINGS_FOLDER}\\settings.json", "r", encoding="utf-8") as settings_file:
        settings_data = json.load(settings_file)

    return {
        "window_color": settings_data["window_color"],
        "frame_color": settings_data["frame_color"],
        "button_color_muted": settings_data["button_color_muted"],
        "button_color": settings_data["button_color"],
        "button_color_highlighted": settings_data["button_color_highlighted"],
        "text_color": settings_data["text_color"],
    }


def restart_program():
    """
    Restarts the application to apply new settings.

    :return: New instance of the app.
    """
    os.startfile("ProjectView.pyw")
    sys.exit()
