import gi

gi.require_version("Adw", "1")
from gi.repository import Adw

from ..structures import ColorExpanderRow, PreferencesGroup, SpinRow, SwitchRow

general_page = Adw.PreferencesPage.new()

# Gaps
settings_gaps = PreferencesGroup("Gaps", "Change gaps in &amp; out, workspaces.")
settings_gaps_in = SpinRow("Gaps In", "Gaps between windows.", "general:gaps_in")
settings_gaps_out = SpinRow(
    "Gaps Out", "Gaps between windows and monitor edges.", "general:gaps_out"
)
settings_gaps_workspaces = SpinRow(
    "Gaps Workspaces",
    "Gaps between workspaces. Stacks with gaps_out.",
    "general:gaps_workspaces",
)

# Borders
settings_borders = PreferencesGroup("Borders", "Size, resize, floating...")

settings_borders_border_size = SpinRow(
    "Border Size", "Size of the border around windows.", "general:border_size"
)

settings_borders_noborder_onfloating = SwitchRow(
    "Border on Floating",
    "Enable borders for floating windows.",
    "general:no_border_on_floating",
    invert=True,
)

settings_borders_resize_onborder = SwitchRow(
    "Resize on Border",
    "Enables resizing windows by clicking and dragging on borders and gaps.",
    "general:resize_on_border",
)

settings_borders_extend_border = SpinRow(
    "Extend Border Grab Area",
    "Extends the area around the border where you can click and drag on, only used when <b><tt>general:resize_on_border</tt></b> is on.",
    "general:extend_border_grab_area",
)

settings_borders_hover_icon_onborder = SwitchRow(
    "Hover Icon on Border",
    "Show a cursor icon when hovering over borders, only used when <b><tt>general:resize_on_border</tt></b> is on.",
    "general:hover_icon_on_border",
)


# Colors

settings_colors = PreferencesGroup("Colors", "Change borders colors.")

settings_colors_inactive_border = ColorExpanderRow(
    "Inactive Border Color",
    "Border color for inactive windows.",
    "general:col.inactive_border",
)

settings_colors_active_border = ColorExpanderRow(
    "Active Border Color",
    "Border color for active windows.",
    "general:col.active_border",
)

settings_colors_nogroup_border = ColorExpanderRow(
    "No Group Border Color",
    "Inactive border color for window that cannot be added to a group.",
    "general:col.nogroup_border",
)

settings_colors_nogroup_active_border = ColorExpanderRow(
    "No Group Active Border Color",
    "Active border color for window that cannot be added to a group.",
    "general:col.nogroup_border_active",
)


for i in [
    settings_gaps_in,
    settings_gaps_out,
    settings_gaps_workspaces,
]:
    settings_gaps.add(i.instance)


for i in [
    settings_borders_border_size,
    settings_borders_noborder_onfloating,
    settings_borders_resize_onborder,
    settings_borders_extend_border,
    settings_borders_hover_icon_onborder,
]:
    settings_borders.add(i.instance)


for i in [
    settings_colors_inactive_border,
    settings_colors_active_border,
    settings_colors_nogroup_border,
    settings_colors_nogroup_active_border,
]:
    settings_colors.add(i)

# Layout
for i in [
    settings_gaps,
    settings_borders,
    settings_colors,
]:
    general_page.add(i)
