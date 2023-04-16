"""
Utilities used by the app window.
"""
import json
import os
import re
import sys


APPLICATION_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
PROJECTS_FOLDER = os.path.join(APPLICATION_DIR, "ProjectView\\projects")
PROJECTS_BACKUP_FOLDER = os.path.join(APPLICATION_DIR, "ProjectView\\projects\\backups")


def get_project_names():
    """
    Reads the items in the projects folder and returns a list
        of settings file names with extension or
        None if no settings files found.
    Called right after app is created.

    :return: List of settings name and extension (list str) or None.
    """
    # Get list of items in project folder
    files = os.listdir(PROJECTS_FOLDER)
    # Filter for json files
    project_names = [file for file in files if file.endswith(".json")]

    return project_names if len(project_names) >= 1 else None


def get_fresh_project_settings():
    """
    Returns a nested dictionary containing the name as outer key and
        widgets information as inner keys.
    Called right after app is created and when add_new_project() is called.

    :return: Nested dictionary with widget containing empty lists.
    """
    return {
            "application_names": [],
            "application_targets": [],
            "directory_names": [],
            "directory_targets": [],
            "website_names": [],
            "website_targets": []
        }


def get_current_project_settings(application_buttons, directory_buttons,
                                 website_buttons):
    """
    Gets project user widget information from buttons lists and returns it as a dictionary.
    Called by save_project() or rename_project().

    :param application_buttons: List of user application buttons info (list str class).
    :param directory_buttons: List of user directory buttons info (list str class).
    :param website_buttons: List of user website buttons info (list str class).

    :return: Dictionary with settings names as keys and
        a list of settings as values (dict list).
    """
    # Buttons are added in pairs for easy delete, so must alternate here
    return {
            "application_names": [x[0] for i, x in enumerate(application_buttons) if i % 2 == 0],
            "application_targets": [x[1] for i, x in enumerate(application_buttons) if i % 2 == 0],
            "directory_names": [x[0] for i, x in enumerate(directory_buttons) if i % 2 == 0],
            "directory_targets": [x[1] for i, x in enumerate(directory_buttons) if i % 2 == 0],
            "website_names": [x[0] for i, x in enumerate(website_buttons) if i % 2 == 0],
            "website_targets": [x[1] for i, x in enumerate(website_buttons) if i % 2 == 0]
        }


def get_project_widgets_info(project_name):
    """
    Gets a profiles user widgets information.
    Called right after app is created or
        change_project() is called.

    :param project_name: Name of a project (str).

    :return: Names and targets of the users project widgets (str).
    """
    with open(f"{PROJECTS_FOLDER}\\{project_name}.json", "r", encoding="utf-8") as active_project_setting:
        project_data = json.load(active_project_setting)
        app_names = project_data["application_names"]
        app_targets = project_data["application_targets"]
        directory_names = project_data["directory_names"]
        directory_targets = project_data["directory_targets"]
        website_names = project_data["website_names"]
        website_targets = project_data["website_targets"]

    return app_names, app_targets,\
        directory_names, directory_targets,\
        website_names, website_targets


def backup_current_project_settings(project_name):
    """
    Gets a project name,
        removes the backup and
        makes a new backup in the project_backup folder.
    Called when remove_project() or save_project() is called.

    :param project_name: Name of a project (str).
    """
    # Check if backup exists and if so removes it
    if os.path.isfile(f"{PROJECTS_BACKUP_FOLDER}\\{project_name}_backup.json"):
        os.remove(f"{PROJECTS_BACKUP_FOLDER}\\{project_name}_backup.json")

    # Save current settings into backup
    if os.path.isfile(f"{PROJECTS_FOLDER}\\{project_name}.json"):
        os.rename(f"{PROJECTS_FOLDER}\\{project_name}.json",
                  f"{PROJECTS_BACKUP_FOLDER}\\{project_name}_backup.json")


def save_current_project_settings(project_settings, project_name):
    """
    Saves the projects current settings
    Called right after app is created or
        add_new_project() or
        save_project() or
        rename_project is called.

    :param project_settings: Dictionary received from get_fresh_profile_settings() or
        get_current_project_settings() (dict).
    :param project_name: Name of a project (str).
    """
    json_settings = json.dumps(project_settings, indent=4)
    with open(f"{PROJECTS_FOLDER}\\{project_name}.json", "w", encoding="utf-8") as save_file:
        save_file.write(json_settings)


def is_name_accepted(new_name, name_list):
    """
    Checks if new name is used in the current frame or projects and
        meets regex requirements or not.
    Called when add_new_project() or
        rename_project() or
        get_new_action_button_info() is called.

    :param new_name: User prompted new name (str).
    :param name_list: List of active buttons in the current frame or
        list of project names (list).

    :return: True if name is accepted else False
    """
    # Check if name is unique
    if new_name not in name_list:
        # Check if name meets regex requirements
        regex = r'^[a-zA-Z0-9_ -]{3,20}$'

        # Check max length of name
        if len(new_name) <= 20:
            # Check regex
            return bool(re.match(regex, new_name))

    return False
