"""
Application main window.
"""
from math import ceil
import os
import webbrowser

from functools import partial
from tkinter import filedialog, messagebox
import customtkinter as ctk

from ProjectView.extra_settings_window import SettingsView
# Utilities
from ProjectView.utilities.app_window_utils import is_name_accepted, get_fresh_project_settings, \
    save_current_project_settings, backup_current_project_settings, get_project_widgets_info, \
    get_current_project_settings
# Variables
from ProjectView.app_variables.messages import NEW_NAME_TEXT, NEW_NAME_NOT_ACCEPTED_TEXT, \
    REMOVE_PROJECT_TEXT, NEW_WEBSITE_ADDRESS_TEXT, OPEN_TARGET_ERROR_TEXT, UNEXPECTED_ERROR_TEXT, \
    INVALID_TARGET_TEXT
from ProjectView.app_variables.settings import FRAME_COLOR, TEXT_COLOR, BUTTON_COLOR_MUTED, \
    BUTTON_COLOR_HIGHLIGHTED, WINDOW_COLOR, BUTTON_COLOR


# Title bar color setting
ctk.set_appearance_mode("Dark")


class AppWindow(ctk.CTk):
    """
    Class used for loading and displaying live widgets.
    Only initial gui setup is stored here.
    All projects and their information are stored as json and
     are loaded in after each project switch.
    """

    def __init__(self):
        super().__init__()
        # Window settings
        self.title("ProjectView")
        self.geometry("-9-1")
        self.resizable(width=False,
                       height=False)
        self.toplevel_window = None
        self.always_on_top_text = ""

        # Stores projects information
        self.project_names = []
        self.current_project_name = None

        # Stores frames information
        self.frames = []
        self.frame_names = ["Settings", "Applications", "Paths", "Websites"]

        # Stores basic widgets information
        self.basic_widgets = []

        # Stores user widgets information
        self.user_widget_names = []
        self.application_widgets = []
        self.directory_widgets = []
        self.website_widgets = []

        # Stores settings frame information
        self.settings_widgets = []
        self.settings_widgets_info = [
            ["Settings", 190, self.open_extra_settings_window, 0, 0, 2, (33, 30), (15, 3)],
            ["Add", 90, self.add_new_project, 1, 0, 1, (33, 3), (3, 3)],
            ["Remove", 90, self.remove_project, 1, 1, 1, (3, 30), (3, 3)],
            ["Save", 90, self.save_project, 3, 0, 1, (33, 3), (3, 15)],
            ["Rename", 90, self.rename_project, 3, 1, 1, (3, 30), (3, 15)]
        ]

    # ------------------------------------------------------------------------ #
    # ------------------------- DEFAULT WIDGETS ------------------------------ #
    def create_frames(self):
        """
        Creates and places a frame in the main window
            for each item in self.frame_names.
        Default = 4.
        """
        for i, v in enumerate(self.frame_names):
            self.frames.append(ctk.CTkFrame(self,
                                            fg_color=FRAME_COLOR))
            self.frames[-1].grid(row=i,
                                 column=0,
                                 padx=(15, 15),
                                 pady=(15, 15 if i == len(self.frame_names) - 1 else 0),
                                 sticky="nsew")

    def create_settings_widgets(self):
        """
        Creates and places a settings widget in the settings frame
        for each item in self.settings_widgets_info.
        Default = 'Extra settings', 'Add', 'Remove', 'Change project', 'Save' and 'Rename'.
        """
        for widget in self.settings_widgets_info:
            # Create button widgets
            self.settings_widgets.append(
                ctk.CTkButton(
                    self.frames[0],
                    text=widget[0],
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_COLOR,
                    fg_color=BUTTON_COLOR_MUTED,
                    hover_color=BUTTON_COLOR_HIGHLIGHTED,
                    width=widget[1],
                    height=12,
                    command=widget[2]
                )
            )
            # Place button widgets
            self.settings_widgets[-1].grid(
                row=widget[3],
                column=widget[4],
                columnspan=widget[5],
                padx=widget[6],
                pady=widget[7]
            )

        # Create project select widget
        self.settings_widgets.append(
            ctk.CTkOptionMenu(
                self.frames[0],
                values=self.project_names,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_COLOR,
                dropdown_text_color=TEXT_COLOR,
                fg_color=BUTTON_COLOR_MUTED,
                button_color=BUTTON_COLOR_MUTED,
                button_hover_color=BUTTON_COLOR_HIGHLIGHTED,
                dropdown_fg_color=BUTTON_COLOR_MUTED,
                dropdown_hover_color=BUTTON_COLOR_HIGHLIGHTED,
                width=190,
                height=30,
                command=self.change_project
            )
        )
        # Place project select widget
        self.settings_widgets[-1].grid(row=2,
                                       column=0,
                                       columnspan=2,
                                       padx=(33, 30),
                                       pady=(3, 3))

    def create_basic_widgets(self):
        """
        Creates and places a basic widget in each frame except the settings frame.
        A basic widget is a '+' button to add a new action and a frame name label.
        """
        # Loop over the frames and frame names to get correct label text and action type
        # i + 1 represents the frame number and thus the type of action (open file, dir or website)
        for i, (frame, frame_name) in enumerate(zip(self.frames[1:], self.frame_names[1:])):
            # Add '+' button
            self.basic_widgets.append(
                ctk.CTkButton(
                    frame,
                    text="+",
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    ),
                    text_color=TEXT_COLOR,
                    fg_color=BUTTON_COLOR_MUTED,
                    width=30,
                    height=25,
                    command=partial(self.place_new_action_button, i + 1)
                )
            )
            # Place '+' button
            self.basic_widgets[-1].grid(
                row=0,
                column=0,
                padx=(17, 10),
                pady=(15, 10)
            )

            # Add frame name label
            self.basic_widgets.append(
                ctk.CTkLabel(
                    frame,
                    text=frame_name,
                    font=ctk.CTkFont(size=16),
                    text_color=TEXT_COLOR,
                    height=25,
                )
            )
            # Place frame name label
            self.basic_widgets[-1].grid(
                row=0,
                column=1,
                padx=(10, 15),
                pady=(15, 10),
                sticky="w"
            )

    # ------------------------------------------------------------------------- #
    # ------------------------- SETTINGS WIDGETS ------------------------------ #
    def open_extra_settings_window(self):
        """
        Opens a new window with extra settings.
        This creates an instance of SettingsView and the menu is generated live.
        :return: SettingsView()
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # Create window if its None or destroyed
            self.toplevel_window = SettingsView(self)
            self.toplevel_window.configure(fg_color=WINDOW_COLOR)

        # Focus window
        self.toplevel_window.focus()

    def add_new_project(self):
        """
        Prompts user for new project name,
            adds it to the menu,
            loads fresh project,
            sets current project name and
            calls change_project().
        """
        while True:
            # Prompt user for a name
            new_project_name = ctk.CTkInputDialog(title="New action",
                                                  text=NEW_NAME_TEXT,
                                                  ).get_input()
            if is_name_accepted(new_name=new_project_name, name_list=self.project_names):
                # Name accepted
                break

            # Name not allowed, display error
            messagebox.showwarning(title="Warning",
                                   message=NEW_NAME_NOT_ACCEPTED_TEXT)

        # Add new name to menu
        self.project_names.append(new_project_name)
        self.settings_widgets[-1].configure(values=self.project_names)

        # Get fresh settings file and save it
        fresh_project_settings = get_fresh_project_settings()
        save_current_project_settings(project_settings=fresh_project_settings,
                                      project_name=new_project_name)

        # Set new project as current project and load it
        self.current_project_name = new_project_name
        self.change_project(new_project_name=new_project_name)

    def remove_project(self):
        """
        Prompts the user if tey are sure.
        Removes the project that is currently displayed and
            makes a backup of the removed project.
        If it is the last project, a fresh one will be created.
        Calls change_project() to load a different profile.
        """
        # Ask if user is sure
        answer = ctk.CTkInputDialog(text=REMOVE_PROJECT_TEXT + self.current_project_name,
                                    title="Remove project?",
                                    ).get_input().lower()
        # User made a mistake and wants to cancel
        if answer.lower() == "stop":
            return

        # Make a backup of the project
        backup_current_project_settings(project_name=self.current_project_name)

        # Update project names list
        self.project_names.remove(self.current_project_name)

        # Create fresh profile if no profiles exist.
        if len(self.project_names) == 0:
            fresh_project_settings = get_fresh_project_settings()
            save_current_project_settings(project_settings=fresh_project_settings,
                                          project_name="New Project")
            self.project_names.append("New Project")

        # Update project menu
        self.settings_widgets[-1].configure(values=self.project_names)

        # Switch project
        self.change_project(new_project_name=self.project_names[0])

    def change_project(self, new_project_name):
        """
        Destroys non default widgets,
            creates and places new project widgets,
            sets new projects name in select menu.

        :param new_project_name: Current profile name in the select menu (str).
        """
        # Destroy non default widgets
        for button in reversed(self.application_widgets):
            button[2].destroy()
        for button in reversed(self.directory_widgets):
            button[2].destroy()
        for button in reversed(self.website_widgets):
            button[2].destroy()

        # Clear trackers
        self.user_widget_names = []
        self.website_widgets = []
        self.directory_widgets = []
        self.application_widgets = []

        # Set new project name
        self.settings_widgets[-1].set(new_project_name)
        self.current_project_name = new_project_name

        # Get project information
        app_names_, app_targets_, \
            directory_names_, directory_targets_, \
            website_names_, website_targets_ = \
            get_project_widgets_info(project_name=new_project_name)

        # Create application buttons
        for app_name_, app_target_ in zip(app_names_, app_targets_):
            self.place_new_action_button(frame_index=1,
                                         new_button_name=app_name_,
                                         new_target=app_target_,
                                         frame=self.frames[1],
                                         widget_list=self.application_widgets)

        # Create directory buttons
        for dir_name_, dir_target_ in zip(directory_names_, directory_targets_):
            self.place_new_action_button(frame_index=2,
                                         new_button_name=dir_name_,
                                         new_target=dir_target_,
                                         frame=self.frames[2],
                                         widget_list=self.directory_widgets)

        # Create website buttons
        for web_name_, web_target_ in zip(website_names_, website_targets_):
            self.place_new_action_button(frame_index=3,
                                         new_button_name=web_name_,
                                         new_target=web_target_,
                                         frame=self.frames[3],
                                         widget_list=self.website_widgets)

    def save_project(self):
        """
        Gets current profile name,
            deletes old backup,
            makes a new backup,
            saves current project settings.
        """
        # Get current project settings
        current_project_settings = get_current_project_settings(
            application_buttons=self.application_widgets,
            directory_buttons=self.directory_widgets,
            website_buttons=self.website_widgets
        )

        # Backup and save
        backup_current_project_settings(project_name=self.current_project_name)
        save_current_project_settings(project_settings=current_project_settings,
                                      project_name=self.current_project_name)

    def rename_project(self):
        """
        Gets current project name,
            validates new name,
            renames the project,
            updates project menu,
            saves settings under new project name,
            calls change_project().
        """
        current_project_name = self.current_project_name

        while True:
            # Prompt user for a new name
            new_project_name = ctk.CTkInputDialog(title="New action",
                                                  text=NEW_NAME_TEXT,
                                                  ).get_input()
            if is_name_accepted(new_name=new_project_name, name_list=self.project_names):
                # Name accepted
                break

            # Name not allowed, display error
            messagebox.showwarning(title="Warning",
                                   message=NEW_NAME_NOT_ACCEPTED_TEXT)

        # Find project to rename and rename it
        for i, project in enumerate(self.project_names):
            if project == current_project_name:
                # noinspection PyUnboundLocalVariable
                self.project_names[i] = new_project_name

        # Update options menu
        self.settings_widgets[-1].configure(values=self.project_names)

        # Get profile settings
        profile_settings = get_current_project_settings(
            application_buttons=self.application_widgets,
            directory_buttons=self.directory_widgets,
            website_buttons=self.website_widgets
        )

        # Save new profile settings
        save_current_project_settings(project_settings=profile_settings,
                                      project_name=new_project_name)

        # Set new project to current project
        self.current_project_name = new_project_name

        # Change project to reload settings
        self.change_project(new_project_name=new_project_name)

    # --------------------------------------------------------------------- #
    # ------------------------- USER WIDGETS ------------------------------ #
    def get_new_action_button_info(self, frame_index):
        """
        Prompts user to give the button a unique name and
            prompts user for a target location.

        :param frame_index: Number to identify the correct frame (int),
            received from basic widget button.

        :returns: List containing the name, target, frame and widget list it belongs to.
        """
        while True:
            # Prompt user for a name
            new_button_name = ctk.CTkInputDialog(title="New action",
                                                 text=NEW_NAME_TEXT,
                                                 ).get_input()
            if is_name_accepted(new_name=new_button_name, name_list=self.user_widget_names):
                # Name accepted
                break

            # Name not allowed, display error
            messagebox.showwarning(title="Warning",
                                   message=NEW_NAME_NOT_ACCEPTED_TEXT)

        # Update user widget name list
        # noinspection PyUnboundLocalVariable
        self.user_widget_names.append(new_button_name)

        # Check what frame the user wants to add the action button to
        if frame_index == 1:
            # Prompt user for a file location
            new_target = filedialog.askopenfilename(title="Select a File",
                                                    initialdir="/",
                                                    filetypes=(("all files", "*.*"),
                                                               ("Text files", "*.txt*")))
            frame = self.frames[1]
            widget_list = self.application_widgets
            if new_target == "":
                return None

        elif frame_index == 2:
            # Prompt user for a folder location
            new_target = filedialog.askdirectory(initialdir="/",
                                                 title="Select a Folder")
            if new_target == "":
                return None
            frame = self.frames[2]
            widget_list = self.directory_widgets

        else:
            # Prompt user for a website address
            new_target = ctk.CTkInputDialog(title="Website address",
                                            text=NEW_WEBSITE_ADDRESS_TEXT,
                                            ).get_input()
            if new_target == "":
                return None
            frame = self.frames[3]
            widget_list = self.website_widgets

        return [new_button_name, new_target, frame, widget_list]

    def place_new_action_button(self, frame_index, new_button_name=False, new_target=False,
                                frame=False, widget_list=False):
        """
        This method is used to place buttons by the app (loading) as well
            by the user (adding new).
        If the user calls this method, self.get_new_action_button_info() is called
            to get the parameters.
        If the app calls this method, parameters are added.
        Appends the new information to the correct widget list.

        :param frame_index: Index of the requested frame (int).

        :param new_button_name: User provided named (str).
        :param new_target: Action bound to the button (open file, path or website)(int).
        :param frame: Frame the button must be placed on (obj).
        :param widget_list: List containing all the frame's buttons (list obj).
        """
        if not any((new_button_name, new_target, frame, widget_list)):
            # No parameters added, prompt user
            new_button_name, new_target, frame, widget_list = self.get_new_action_button_info(
                frame_index)

            if not new_target:
                # User clicked cancel
                messagebox.showerror(title="Invalid target!",
                                     message=INVALID_TARGET_TEXT)
                del self.project_names[-1]
                return

        # Create remove action button
        widget_list.append([
            new_button_name,
            new_target,
            ctk.CTkButton(
                frame,
                text="-",
                width=30,
                height=25,
                fg_color=BUTTON_COLOR_MUTED,
                hover_color=BUTTON_COLOR_HIGHLIGHTED,
                font=ctk.CTkFont(size=12,
                                 weight="bold"),
                text_color=TEXT_COLOR,
                command=partial(self.destroy_user_widgets,
                                new_button_name,
                                widget_list),
            )
        ])
        # Place remove action button
        widget_list[-1][-1].grid(
            row=ceil(len(widget_list) / 2),
            column=0,
            padx=(17, 10),
            pady=(5, 10)
        )

        # Create new action button
        widget_list.append([
            new_button_name,
            new_target,
            ctk.CTkButton(frame,
                          text=new_button_name,
                          width=175,
                          height=25,
                          fg_color=BUTTON_COLOR,
                          hover_color=BUTTON_COLOR_HIGHLIGHTED,
                          font=ctk.CTkFont(size=14),
                          text_color=TEXT_COLOR,
                          command=partial(self.open_target,
                                          frame_index,
                                          new_button_name,
                                          new_target))
        ])
        # Place remove action button
        widget_list[-1][-1].grid(
            row=ceil(len(widget_list) / 2),
            column=1,
            columnspan=2,
            padx=(10, 15),
            pady=(5, 10)
        )

        # Update user widget name list
        self.user_widget_names.append(new_button_name)

    @staticmethod
    def destroy_user_widgets(button_name, widget_list):
        """
        Destroys user button that is passed on.

        :param button_name: Name of the button (str).
        :param widget_list: List of widgets the widget is in.
        """
        for widget in reversed(widget_list):
            if widget[0] == button_name:
                widget[2].destroy()
                widget_list.remove(widget)

    @staticmethod
    def open_target(frame_index, button_name, location):
        """
        Opens target of the user widget connected to it.
        This can be opening a file, path or website.
        In case of an error, appropriate message is displayed.

        :param frame_index: Index of the requested frame (int).
        :param button_name: Name of the pressed button (str).
        :param location: Target of the file, directory or website (str).

        :return: Error message or the target.
        """
        # Check if user wants to open a file
        if frame_index == 1:
            # Check if it's an actual file and user has access
            if not os.path.isfile(location) or not os.access(location, os.R_OK):
                # Cannot open file
                messagebox.showerror(title="Error",
                                     message=f"{OPEN_TARGET_ERROR_TEXT} '{button_name}'")
            # Open file
            os.startfile(location)

        # Check if user wants to open a directory
        elif frame_index == 2:
            # Check if it's an actual directory
            if not os.path.exists(location):
                # directory not found
                messagebox.showerror(title="Error",
                                     message=f"{OPEN_TARGET_ERROR_TEXT} '{location}'")
            # Open directory
            os.startfile(location)

        # User wants to open a website
        else:
            # Try to open the website
            try:
                webbrowser.open(location)
            # website cannot be opened, show error
            except webbrowser.Error:
                messagebox.showerror(title="Error",
                                     message=f"{UNEXPECTED_ERROR_TEXT} '{location}'")
