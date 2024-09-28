from ..imports import Setting, Adw, Gtk, HyprData

from ..widgets import (
    CheckButtonImage,
    ColorExpanderRow,
    InfoButton,
    PreferencesGroup,
    SpinRow,
    SwitchRow,
)

general_page = Adw.PreferencesPage.new()

# Gaps
settings_gaps = PreferencesGroup(
    "Gaps", "Change gaps in/out and gaps between workspaces."
)


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

# Cursor
settings_cursor = PreferencesGroup("Cursor", "Change cursor settings.")

settings_cursor_no_focus_fallback = SwitchRow(
    "No Focus Fallback",
    "If enabled, will not fall back to the next available window when moving focus in a direction where no window was found.",
    "general:no_focus_fallback",
)

# Other
settings_other = PreferencesGroup("", "")

# Layout Chooser Row
settings_other_layout = Adw.ActionRow.new()

# Vertical container
settings_other_layout_container_v = Gtk.Box(
    orientation=Gtk.Orientation.VERTICAL,
    css_classes=["title", "vertical"],
    margin_end=12,
    margin_start=12,
    margin_top=6,
    margin_bottom=6,
)


# Title
settings_other_layout_container_v_title = Gtk.Label(
    label="Layout", css_classes=["title"], halign=Gtk.Align.START
)
# Subtitle
settings_other_layout_container_v_subtitle = Gtk.Label(
    label="Which layout to use.", css_classes=["subtitle"], halign=Gtk.Align.START
)

# Append title & subtitle
settings_other_layout_container_v.append(settings_other_layout_container_v_title)
settings_other_layout_container_v.append(settings_other_layout_container_v_subtitle)

settings_other_layout_container_h = Gtk.Box(
    orientation=Gtk.Orientation.HORIZONTAL, spacing=24, homogeneous=True
)

# Checkbuttons
settings_other_layout_checkbutton_dwindle = CheckButtonImage("Dwindle", "dwindle")

settings_other_layout_checkbutton_master = CheckButtonImage("Master", "master")
settings_other_layout_checkbutton_master.checkbutton.set_group(
    settings_other_layout_checkbutton_dwindle.checkbutton
)


default = HyprData.get_option("general:layout")

if not default:
    HyprData.new_option(Setting("general:layout", "dwindle"))
    default = "dwindle"  # type: ignore
else:
    default = default.value

if default == "master":
    settings_other_layout_checkbutton_master.checkbutton.set_active(True)
else:
    settings_other_layout_checkbutton_dwindle.checkbutton.set_active(True)


settings_other_layout_container_h.append(settings_other_layout_checkbutton_dwindle)
settings_other_layout_container_h.append(settings_other_layout_checkbutton_master)

# Append hbox to vbox
settings_other_layout_container_v.append(settings_other_layout_container_h)

settings_other_layout.set_child(settings_other_layout_container_v)

#
settings_other_allow_tearing = SwitchRow(
    "Allow Tearing",
    "Master switch for allowing tearing to occur. See the <a href='https://wiki.hyprland.org/Configuring/Tearing/'>Tearing Page</a>.",
    "general:allow_tearing",
)

settings_other.add(settings_other_layout)
settings_other.add(settings_other_allow_tearing)


# Add Cursor settings
for i in [
    settings_cursor_no_focus_fallback,
]:
    settings_cursor.add(i)


# Add Gaps settings
for i in [settings_gaps_in, settings_gaps_out, settings_gaps_workspaces]:
    settings_gaps.add(i)


# Add Border settings
for i in [
    settings_borders_border_size,
    settings_borders_noborder_onfloating,
    settings_borders_resize_onborder,
    settings_borders_extend_border,
    settings_borders_hover_icon_onborder,
]:
    settings_borders.add(i)


# Add Color settings
for i in [
    settings_colors_inactive_border,
    settings_colors_active_border,
    settings_colors_nogroup_border,
    settings_colors_nogroup_active_border,
]:
    settings_colors.add(i)


# Add sections
for i in [
    settings_gaps,
    settings_borders,
    settings_colors,
    settings_cursor,
    settings_other,
]:
    general_page.add(i)
