from ..widgets import (
    PreferencesGroup,
    SwitchRow,
    BezierGroup,
    InfoButton,
    ExpanderRow,
)
from ..imports import Adw


animations_page = Adw.PreferencesPage.new()


settings_animations = PreferencesGroup("", "")
settings_animations.add(
    SwitchRow(
        "Animations Enabled",
        "Enable animations.",
        "animations:enabled",
    )
)

settings_animations.add(
    SwitchRow(
        "First Launch Animation",
        "Enable first launch animation.",
        "animations:first_launch_animation",
    )
)

settings_bezier = BezierGroup()
settings_anim_tree = PreferencesGroup(
    "Animation Tree",
    "Animation tree for windows, layers, border and workspaces.",
)
settings_anim_tree_windows = ExpanderRow("Windows", "")
settings_anim_tree_windows_windowsIn = ExpanderRow("Windows In", "Window open")
settings_anim_tree_windows_windowsOut = ExpanderRow("Windows Out", "Window close")
settings_anim_tree_windows_windowsMove = ExpanderRow(
    "Windows In", "Everything in between, moving, dragging and resizing."
)


settings_anim_tree.set_header_suffix(
    InfoButton(
        "The animations are a tree. If an animation is unset, it will inherit its parent’s values."
    )
)

for i in [
    settings_anim_tree_windows_windowsIn,
    settings_anim_tree_windows_windowsOut,
    settings_anim_tree_windows_windowsMove,
]:
    settings_anim_tree_windows.add_row(i)

for i in [
    settings_anim_tree_windows,
]:
    settings_anim_tree.add(i)


for i in [settings_animations, settings_bezier, settings_anim_tree]:
    animations_page.add(i)
