from ...structures import Adw, PreferencesGroup, SpinRow, SwitchRow

blur_page = Adw.NavigationPage.new(Adw.PreferencesPage.new(), title="TEEEEST")
blur_page.set_tag("blur-page")
blur_page_content: Adw.PreferencesPage = blur_page.get_child()  # type: ignore


settings_blur = PreferencesGroup("", "")

settings_blur_size = SpinRow(
    "Blur Size", "Blur size (distance).", "decoration:blur:size"
)
settings_blur_passes = SpinRow(
    "Blur Passes", "The amount of passes to perform.", "decoration:blur:passes"
)

settings_blur_ignore_opacity = SwitchRow(
    "Ignore Opacity",
    "Make the blur layer ignore the opacity of the window.",
    "decoration:blur:ignore_opacity",
)
settings_blur_new_optimizations = SwitchRow(
    "New Optimizations",
    "Whether to enable further optimizations to the blur. Recommended to leave on, as it will massively improve performance.",
    "decoration:blur:new_optimizations",
)
settings_blur_xray = SwitchRow(
    "Blur Xray",
    "If enabled, floating windows will ignore tiled windows in their blur. Only available if blur_new_optimizations is true. Will reduce overhead on floating blur significantly.",
    "decoration:blur:xray",
)

settings_blur_noise = SpinRow(
    "Blur Noise",
    "How much noise to apply.",
    "decoration:blur:noise",
    data_type=float,
    max=1,
    decimal_digits=4,
)
settings_blur_contrast = SpinRow(
    "Blur Contrast",
    "Contrast modulation for blur.",
    "decoration:blur:contrast",
    data_type=float,
    max=2,
    decimal_digits=4,
)
settings_blur_brightness = SpinRow(
    "Blur Brightness",
    "Brightness modulation for blur.",
    "decoration:blur:brightness",
    data_type=float,
    max=2,
    decimal_digits=4,
)
settings_blur_vibrancy = SpinRow(
    "Vibrancy",
    "Increase saturation of blurred colors.",
    "decoration:blur:vibrancy",
    data_type=float,
    max=1,
    decimal_digits=4,
)
settings_blur_vibrancy_darkness = SpinRow(
    "Vibrancy Darkness",
    "How strong the effect of <b><tt>vibrancy</tt></b> is on dark areas.",
    "decoration:blur:vibrancy_darkness",
    data_type=float,
    max=1,
    decimal_digits=4,
)
settings_blur_special = SwitchRow(
    "Blur Special",
    "Whether to blur behind the special workspace (note: expensive).",
    "decoration:blur:special",
)
settings_blur_popups = SwitchRow(
    "Blur Popups",
    "Whether to blur popups (e.g. right-click menus).",
    "decoration:blur:popups",
)
settings_blur_popups_ignorealpha = SpinRow(
    "Popups Ignore Alpha",
    "Works like ignorealpha in layer rules. If pixel opacity is below set value, will not blur.",
    "decoration:blur:popups_ignorealpha",
    data_type=float,
    max=1,
)


for i in [
    # settings_blur_enabled,
    settings_blur_size,
    settings_blur_passes,
    settings_blur_ignore_opacity,
    settings_blur_new_optimizations,
    settings_blur_xray,
    settings_blur_noise,
    settings_blur_contrast,
    settings_blur_brightness,
    settings_blur_vibrancy,
    settings_blur_vibrancy_darkness,
    settings_blur_special,
    settings_blur_popups,
    settings_blur_popups_ignorealpha,
]:
    if hasattr(i, "instance"):
        settings_blur.add(i.instance)
        continue
    settings_blur.add(i)

settings_blur_enabled = PreferencesGroup(
    "",
    "",
)
settings_blur_enabled.add(
    SwitchRow(
        "Blur Enabled",
        "Enable kawase window background blur.",
        "decoration:blur:enabled",
    ).instance
)


blur_page_content.add(settings_blur_enabled)
blur_page_content.add(settings_blur)
