from ..structures import Adw, PreferencesGroup, SpinRow, SwitchRow

decoration_page = Adw.PreferencesPage.new()

settings_rounding = PreferencesGroup("", "")

settings_rounding_spinrow = SpinRow(
    "Rounding", "Rounded corners’ radius (in layout px).", "decoration:rounding"
)
settings_rounding.add(settings_rounding_spinrow.instance)

settings_opacity = PreferencesGroup(
    "Opacity", "Active, inactive and fullscreen opacity."
)
settings_opacity_active = SpinRow(
    "Active Opacity",
    "Opacity of active windows.",
    "decoration:active_opacity",
    float,
    max=1.0,
)
settings_opacity_inactive = SpinRow(
    "Inactive Opacity",
    "Opacity of inactive windows.",
    "decoration:inactive_opacity",
    float,
    max=1.0,
)
settings_opacity_fullscreen = SpinRow(
    "Fullscreen Opacity",
    "Opacity of fullscreen windows.",
    "decoration:fullscreen_opacity",
    float,
)

settings_shadow = PreferencesGroup("Shadow", "Drop shadow, range, power and colors.")
settings_shadow_range = SpinRow(
    "Shadow Range",
    "Shadow range (“size”) in layout px.",
    "decoration:shadow_range",
)
settings_shadow_ignore_window = SwitchRow(
    "Shadow Ignore Window",
    "If enabled, the shadow will not be rendered behind the window itself, only around it.",
    "decoration:shadow_ignore_window",
)

for i in [
    settings_shadow_ignore_window,
    settings_shadow_range,
]:
    if hasattr(i, "instance"):
        settings_shadow.add(i.instance)
        continue
    settings_shadow.add(i)

for i in [
    settings_opacity_active,
    settings_opacity_inactive,
    settings_opacity_fullscreen,
]:
    settings_opacity.add(i.instance)


for i in [settings_rounding, settings_opacity, settings_shadow]:
    decoration_page.add(i)
