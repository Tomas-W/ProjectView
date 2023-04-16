"""
Initializes the Application Window by loading the default widgets.
If a profile is found, settings will be applied.
"""
# Utilities
from ProjectView.utilities.app_window_utils import get_project_names, get_fresh_project_settings, \
    save_current_project_settings, get_project_widgets_info
# Variables
from ProjectView.app_variables.settings import WINDOW_COLOR
from .utilities.general_utils import get_user_setting

from .app_window import AppWindow


app = AppWindow()

# Set project names and current project name
if get_project_names() is not None:
    # Projects found
    app.project_names = [project_name.split(".")[0] for project_name in get_project_names()]
    app.current_project_name = app.project_names[0]
else:
    # No projects present, create new one
    app.project_names = ["New Project"]
    app.current_project_name = "New Project"
    # Create and save new profile
    new_project_settings = get_fresh_project_settings()
    save_current_project_settings(project_settings=new_project_settings,
                                  project_name=app.current_project_name)

# Create default frames
app.create_frames()

# Create default settings widgets
app.create_settings_widgets()

# Create default basic widgets
app.create_basic_widgets()

# Load project widgets information
# If no profiles present, a blank project is created
app_names, app_targets, directory_names, directory_targets, website_names, website_targets = \
    get_project_widgets_info(project_name=app.current_project_name)

# Create application widgets
for name, target in zip(app_names, app_targets):
    app.place_new_action_button(frame_index=1,
                                new_button_name=name,
                                new_target=target,
                                frame=app.frames[1],
                                widget_list=app.application_widgets)

# Create directory widgets
for name, target in zip(directory_names, directory_targets):
    app.place_new_action_button(frame_index=2,
                                new_button_name=name,
                                new_target=target,
                                frame=app.frames[2],
                                widget_list=app.directory_widgets)

# Create website widgets
for name, target in zip(website_names, website_targets):
    app.place_new_action_button(frame_index=3,
                                new_button_name=name,
                                new_target=target,
                                frame=app.frames[3],
                                widget_list=app.website_widgets)

# Get and apply window on top setting
always_on_top = get_user_setting(setting="always_on_top")
if always_on_top == "True":
    app.attributes('-topmost', True)

# Load always on top text
app.always_on_top_text = get_user_setting("always_on_top_text")

# Apply window background color
app.configure(fg_color=WINDOW_COLOR)

app.mainloop()
