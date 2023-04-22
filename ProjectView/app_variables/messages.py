"""
Stores messages to be displayed in the apps messagebox.
"""
NEW_NAME_TEXT = "Provide a name" \
                "\n\n" \
                "Allowed:\n" \
                "  az-AZ\n" \
                "  0-9\n" \
                "  - or _\n" \
                "  spacebar\n\n" \
                "Requirements:\n" \
                "  Min 3 characters\n" \
                "   Max 20 characters"
NEW_NAME_NOT_ACCEPTED_TEXT = "Name not accepted!\n\n" \
                             "Either name is used already\n" \
                             "or\n" \
                             "Name did not meet requirements"
REMOVE_PROJECT_TEXT = "Type 'stop' to cancel!\n" \
                      "Anything else will trigger delete\n" \
                      "You are about to delete project:\n\n"
NEW_WEBSITE_ADDRESS_TEXT = "Provide a website address:"
RESET_SETTINGS_TEXT = "Type 'stop' to cancel!\n" \
                      "Anything else will trigger a reset" \
                      "of the settings in this window!"

CHANGE_COLOR_TEXT = "Provide a color in hex values:\n" \
                    "Input must be 7 characters total\n\n" \
                    "e.g. '#cc10c7'"

OPEN_TARGET_ERROR_TEXT = "Unknown error!\n\n" \
                         "Check:\n" \
                         "Do you have access rights?\n" \
                         "Has the file/folder been removed/renamed?\n\n" \
                         "Cannot open:\n\n"
INVALID_TARGET_TEXT = "Invalid target!\n" \
                      "Try again"

RENAME_ERROR_TEXT = "Unexpected error occurred!\n" \
                    "Cannot rename settings file.\n\n" \
                    "User has no rights to rename the file\n" \
                    "Try again and if problem persists,\n" \
                    "choose a different name or reset the program"
UNEXPECTED_RENAME_ERROR_TEXT = "Unexpected error occurred!\n\n" \
                        "Try again or save profile folder and " \
                        "reinstall if problem persists"
