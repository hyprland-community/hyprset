from ...structures import (Adw, ButtonRow, ColorEntryRow, Icon,
                           PreferencesGroup, SpinRow, SwitchRow)
from .blur import blur_page

index_page = Adw.NavigationPage.new(Adw.PreferencesPage.new(), title="TEEEEST")
index_page.set_tag("index-page")
#
index_page_content: Adw.PreferencesPage = index_page.get_child()  # type:ignore

decoration_page = Adw.NavigationView.new()
decoration_page.add(index_page)
decoration_page.add(blur_page)

# NavigationView -> NavigationPage -> PreferencesPage -> PreferencesGroup
# index_page = Adw.NavigationPage.new()

settings_rounding = PreferencesGroup("", "")

settings_rounding_spinrow = SpinRow(
    "Rounding", "Rounded corners' radius (in layout px).", "decoration:rounding"
)
settings_rounding.add(settings_rounding_spinrow.instance)

settings_opacity = PreferencesGroup(
    "Opacity", "Active, inactive and fullscreen opacity."
)
settings_opacity_active = SpinRow(
    "Active Opacity",
    "Opacity of active windows.",
    "decoration:active_opacity",
    data_type=float,
    max=1.0,
)
settings_opacity_inactive = SpinRow(
    "Inactive Opacity",
    "Opacity of inactive windows.",
    "decoration:inactive_opacity",
    data_type=float,
    max=1.0,
)
settings_opacity_fullscreen = SpinRow(
    "Fullscreen Opacity",
    "Opacity of fullscreen windows.",
    "decoration:fullscreen_opacity",
    data_type=float,
    max=1.0,
)

settings_shadow = PreferencesGroup("Shadow", "Drop shadow, range, power and colors.")
settings_shadow_drop_shadow = SwitchRow(
    "Drop Shadow", "Enable drop shadows on windows.", "decoration:drop_shadow"
)
settings_shadow_range = SpinRow(
    "Shadow Range",
    "Shadow range (“size”) in layout px.",
    "decoration:shadow_range",
)
settings_shadow_render_power = SpinRow(
    "Shadow Render Power",
    "In what power to render the falloff (more power, the faster the falloff).",
    "decoration:shadow_render_power",
    min=1,
    max=4,
)


settings_shadow_ignore_window = SwitchRow(
    "Shadow Ignore Window",
    "If enabled, the shadow will not be rendered behind the window itself, only around it.",
    "decoration:shadow_ignore_window",
)
settings_shadow_color = ColorEntryRow(
    "Shadow's Color",
    "Shadow's color. Alpha dictates shadow’s opacity.",
    "decoration:col.shadow",
)
settings_shadow_color_inactive = ColorEntryRow(
    "Inactive Shadow Color",
    "Inactive shadow color. If not set, will fall back to <b><tt>col.shadow</tt></b>.",
    "decoration:col.shadow_inactive",
)
settings_shadow_scale = SpinRow(
    "Shadow's Scale",
    "Shadow's scale.",
    "decoration:shadow_scale",
    max=1.0,
    data_type=float,
)
settings_dim = PreferencesGroup("Dim", "Change dim settings.")
settings_dim_inactive_window = SwitchRow(
    "Inactive Window",
    "Enables dimming of inactive windows.",
    "decoration:dim_inactive",
)
settings_dim_strenght = SpinRow(
    "Dim Strenght",
    "How much inactive windows should be dimmed.",
    "decoration:dim_strength",
    data_type=float,
    max=1.0,
)
settings_dim_special = SpinRow(
    "Dim Special",
    "How much to dim the rest of the screen by when a special workspace is open.",
    "decoration:dim_special",
    data_type=float,
    max=1.0,
)
settings_dim_around = SpinRow(
    "Dim Around",
    "How much the <b><tt>dimaround</tt></b> window rule should dim by.",
    "decoration:dim_around",
    data_type=float,
    max=1.0,
)

for i in [
    settings_dim_inactive_window,
    settings_dim_strenght,
    settings_dim_special,
    settings_dim_around,
]:
    if hasattr(i, "instance"):
        settings_dim.add(i.instance)
        continue
    settings_dim.add(i)


for i in [
    settings_shadow_drop_shadow,
    settings_shadow_range,
    settings_shadow_render_power,
    settings_shadow_ignore_window,
    settings_shadow_color,
    settings_shadow_color_inactive,
    settings_shadow_scale,
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


for i in [settings_rounding, settings_opacity, settings_shadow, settings_dim]:
    index_page_content.add(i)


settings_blur = PreferencesGroup("", "")
settings_blur.add(
    ButtonRow(
        "tool-gradient-conical-symbolic",
        "Blur",
        "Size, passes, noise, contrast, vibrancy...",
        lambda *_: decoration_page.push_by_tag("blur-page"),
    )
)
index_page_content.add(settings_blur)
