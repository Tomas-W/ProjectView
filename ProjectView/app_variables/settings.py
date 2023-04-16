"""
Contains variables associated with application settings.
"""
from ProjectView.utilities.general_utils import get_color_settings


user_setting_dict = get_color_settings()

WINDOW_COLOR = user_setting_dict["window_color"]
FRAME_COLOR = user_setting_dict["frame_color"]
BUTTON_COLOR_MUTED = user_setting_dict["button_color_muted"]
BUTTON_COLOR = user_setting_dict["button_color"]
BUTTON_COLOR_HIGHLIGHTED = user_setting_dict["button_color_highlighted"]
TEXT_COLOR = user_setting_dict["text_color"]
