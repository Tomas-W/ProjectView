"""
Application extra settings window.
"""
import os
import sys
from functools import partial

import customtkinter as ctk
# Utilities
from ProjectView.utilities.extra_settings_window_utils import get_color_palette, is_valid_hex_color,\
    restore_settings_file
from ProjectView.utilities.general_utils import set_user_settings, restart_program, get_user_setting
# Variables
from ProjectView.app_variables.messages import CHANGE_COLOR_TEXT, RESET_SETTINGS_TEXT
from ProjectView.app_variables.settings import WINDOW_COLOR, BUTTON_COLOR_MUTED, \
    BUTTON_COLOR_HIGHLIGHTED, TEXT_COLOR

APPLICATION_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
APP_SETTINGS_FOLDER = os.path.join(APPLICATION_DIR, "ProjectView\\app_settings")
APP_SETTINGS_BACKUP_FOLDER = os.path.join(APPLICATION_DIR, "ProjectView\\app_settings\\backups")


class SettingsView(ctk.CTkToplevel):
    """
    Class used for displaying the extra settings window.
    After user input the app restarts to load the new settings.
    """

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Settings")
        self.geometry("+279-1")  # ("+353+0")
        self.attributes('-topmost', True)
        self.resizable(width=False,
                       height=False)
        self.configure(fg_color=WINDOW_COLOR)

        self.frame_names = app.frame_names

        # Stores general settings information
        self.general_settings_widgets = []
        self.general_settings = [
            [get_user_setting("always_on_top_text"), partial(self.toggle_always_on_top, app)],
            ["Change backgrounds colors", self.change_background_colors],
            ["Change widgets colors", self.change_widget_colors],
            ["Change text color", self.change_text_color],
            ["Reset to default", self.reset_settings],
        ]

        # Currently taken out
        self.frame_settings_widgets = []

        # Create and place general settings widgets
        self.create_general_settings_widgets()

        # Create and place frame setting widgets
        self.create_frame_settings_widgets()

    # ------------------------------------------------------------------------ #
    # ------------------------- DEFAULT WIDGETS ------------------------------ #
    def create_general_settings_widgets(self):
        """
        Places general settings widgets in the extra settings window
            taken from self.general_settings,
            creates widget and
            places them.
        Called when extra settings window is initialized.
        """
        for i, setting in enumerate(self.general_settings):
            # Create button
            self.general_settings_widgets.append(
                ctk.CTkButton(
                    self,
                    text=setting[0],
                    width=200,
                    height=12,
                    font=ctk.CTkFont(size=12),
                    fg_color=BUTTON_COLOR_MUTED,
                    hover_color=BUTTON_COLOR_HIGHLIGHTED,
                    text_color=TEXT_COLOR,
                    command=setting[1],
                )
            )
            # Place button
            self.general_settings_widgets[-1].grid(
                row=i,
                column=0,
                columnspan=3,
                padx=(20, 20),
                pady=(20, 0)
            )

    def create_frame_settings_widgets(self):
        """
        Places frame settings widgets in the settings window
            taken from self.frame_settings,
            creates widget,
            places them.
        Called when extra settings window is initialized.
        """
        row_num = len(self.general_settings)

        # Add label
        self.frame_settings_widgets.append(
            ctk.CTkLabel(
                self,
                text="Organize app frames",
                font=ctk.CTkFont(size=12),
                text_color=TEXT_COLOR,
            )
        )
        # Place label
        self.frame_settings_widgets[-1].grid(
            row=row_num,
            column=0,
            columnspan=2,
            padx=(10, 0),
            pady=(20, 0),
        )
        row_num += 1

        # Add project select widget
        self.frame_settings_widgets.append(
            ctk.CTkOptionMenu(
                self,
                values=self.frame_names[1:],
                font=ctk.CTkFont(size=14),
                text_color=TEXT_COLOR,
                dropdown_text_color=TEXT_COLOR,
                fg_color=BUTTON_COLOR_MUTED,
                button_color=BUTTON_COLOR_MUTED,
                button_hover_color=BUTTON_COLOR_HIGHLIGHTED,
                dropdown_fg_color=BUTTON_COLOR_MUTED,
                dropdown_hover_color=BUTTON_COLOR_HIGHLIGHTED,
                width=200,
                height=30,
                state="disabled",
            )
        )
        # Place project select widget
        self.frame_settings_widgets[-1].grid(row=row_num,
                                             column=0,
                                             columnspan=3,
                                             padx=(20, 20),
                                             pady=(5, 0))
        row_num += 1

        # Create rename and remove widgets
        for i, (text, command) in enumerate(zip(["Rename", "Remove", "Add"],
                                                [self.rename_frame, self.remove_frame,
                                                 self.add_frame])):
            self.frame_settings_widgets.append(
                ctk.CTkButton(
                    self,
                    text=text,
                    width=55,
                    height=12,
                    font=ctk.CTkFont(size=12),
                    fg_color=BUTTON_COLOR_MUTED,
                    hover_color=BUTTON_COLOR_HIGHLIGHTED,
                    text_color=TEXT_COLOR,
                    command=command,
                    state="disabled",
                )
            )
            # Create rename and remove widgets
            self.frame_settings_widgets[-1].grid(
                row=row_num,
                column=i,
                padx=(14 if i == 0 else 0, 14 if i == 2 else 0),
                pady=(10, 20)
            )

    # ----------------------------------------------------------------------------- #
    # ------------------------- TOGGLE ON TOP WIDGET ------------------------------ #
    def toggle_always_on_top(self, app):
        """
        Toggles always-on-top behavior of the app.
        """
        # Check state of always-on-top attribute
        if app.attributes('-topmost'):
            # Always on top is on, switch off
            app.attributes('-topmost', False)
            self.general_settings_widgets[0].configure(text="Always on top is: OFF")
            # Save settings
            set_user_settings(settings=["always_on_top", "always_on_top_text"],
                              values=["False", "Always on top is: OFF"])

        else:
            # Always on top is off, switch on
            app.attributes('-topmost', True)
            self.general_settings_widgets[0].configure(text="Always on top is: ON")
            # Save settings
            set_user_settings(settings=["always_on_top", "always_on_top_text"],
                              values=["False", "Always on top is: ON"])

    # ------------------------------------------------------------------------- #
    # ------------------------- COLOR WIDGETS ------------------------------ #
    @staticmethod
    def change_background_colors():
        """
        Prompts the user for a hex color code,
            calls get_color_palette() to get a lighter tint of the same color,
            sets the window color to the prompted color and
            sets the frame color to the lighter tint.
        Calls self.restart_program() to restart and apply settings.
        """
        while True:
            # Prompt user for a hex color
            new_window_color = ctk.CTkInputDialog(title="Change background colors",
                                                  text=CHANGE_COLOR_TEXT).get_input()
            # Check if color is valid
            if is_valid_hex_color(new_window_color):
                break

        # Get a darker tint of that color
        lighter_frame_color = get_color_palette(new_window_color)[1]

        # Save colors
        set_user_settings(settings=["window_color", "frame_color"],
                          values=[new_window_color, lighter_frame_color])

        # Start a new instance of the app to load new colors
        restart_program()

    @staticmethod
    def change_widget_colors():
        """
        Prompts the user for a hex color code,
            calls get_color_palette() to get a lighter and darker tint of the same color,
            sets button color muted color to the darker tint,
            sets button color to the prompted color and
            sets the button color highlighted color to the lighter tint.
        Calls self.restart_program() to restart and apply settings.
        """
        while True:
            # Prompt user for a hex color
            widget_color = ctk.CTkInputDialog(title="Change widget colors",
                                              text=CHANGE_COLOR_TEXT).get_input()
            # Check if color is valid
            if is_valid_hex_color(widget_color):
                break

        # Get a darker and lighter tint of that color
        new_widget_color = get_color_palette(widget_color)
        darker_widget_color = new_widget_color[0]
        lighter_widget_color = new_widget_color[1]

        # Sve settings
        set_user_settings(settings=["button_color_muted", "button_color", "button_color_highlighted"],
                          values=[darker_widget_color, new_widget_color, lighter_widget_color])

        # Start a new instance of the app to load new colors
        restart_program()

    @staticmethod
    def change_text_color():
        """
        Prompts the user for a hex color code and
            sets it as the text color.
        Calls self.restart_program() to restart and apply settings.
        """
        while True:
            # Prompt user for a hex color
            new_text_color = ctk.CTkInputDialog(title="Change background colors",
                                                text=CHANGE_COLOR_TEXT).get_input()
            # Check if color is valid
            if is_valid_hex_color(new_text_color):
                break

        # Save setting
        set_user_settings(settings=["text_color"],
                          values=[new_text_color])

        # Start a new instance of the app to load new color
        restart_program()

    @staticmethod
    def reset_settings():
        """
        Prompts the user if tey are sure.
        All settings in the extra settings window will be reset to
            their defaults.
        """
        # Ask if user is sure
        answer = ctk.CTkInputDialog(text=RESET_SETTINGS_TEXT,
                                    title="Reset settings?",
                                    ).get_input().lower()
        # User made a mistake and wants to cancel
        if answer.lower() == "stop":
            return

        restore_settings_file(file_path=APP_SETTINGS_FOLDER,
                              backup_path=APP_SETTINGS_BACKUP_FOLDER)

    # ----------------------------------------------------------------------- #
    # ------------------------- FRAME SETTINGS ------------------------------ #
    def rename_frame(self):
        pass

    def remove_frame(self):
        pass

    def add_frame(self):
        pass
