from typing import Literal, Type

from ..imports import (
    Adw,
    Color,
    Gio,
    GLib,
    Gradient,
    Gtk,
    HyprData,
    List,
    Setting,
    Union,
)

# Some widgets have a default value, to check
# if their new value is different from the initial one.
# If it is, then the changes count of the toast is increased;
# if not, then the changes count of the toast is decreased.


class CustomToastOverlay:
    instances: List[
        Union[
            "Adjustment",
            "ColorExpanderRow.ColorEntryRow",
            "ColorEntryRow",
            "ColorExpanderRow",
            "SwitchRow",
        ]
    ] = []

    def __init__(self) -> None:
        self.changes = 0
        self._instance = Adw.ToastOverlay.new()
        self.toast = Adw.Toast.new("You have 0 unsaved changes!")
        self.toast.connect("button-clicked", self.save_changes)
        self.toast.set_button_label("Save now")
        self.toast.set_timeout(0)

    @property
    def instance(self) -> Adw.ToastOverlay:
        return self._instance

    def show_toast(self) -> None:
        self.instance.add_toast(self.toast)

    def hide_toast(self) -> None:
        self.toast.dismiss()

    def add_change(self) -> None:
        self.changes += 1
        self.toast.set_title(f"You have {self.changes} unsaved changes!")
        return self.show_toast()

    def del_change(self) -> None:
        self.changes -= 1
        self.toast.set_title(f"You have {self.changes} unsaved changes!")
        if self.changes == 0:
            return self.hide_toast()

    # After calling this function, each widget updates its new default value.
    def save_changes(self, *_) -> None:
        # if self.changes == 0:
        #    return

        self.changes = 0
        self.hide_toast()

        for i in CustomToastOverlay.instances:
            i.update_default()
        return HyprData.save_all()


ToastOverlay = CustomToastOverlay()


class PreferencesGroup(Adw.PreferencesGroup):
    def __init__(self, title: str, description: str):
        super().__init__()
        self.set_title(title)
        self.set_description(description)


class ColorExpanderRow(Adw.ExpanderRow):
    class ColorEntryRow(Adw.EntryRow):
        def __init__(self, parent: "ColorExpanderRow", new_color: str = ""):
            super().__init__()
            self.parent = parent
            self.set_title("Color")
            ToastOverlay.instances.append(self)

            if new_color:
                self._default = new_color
                self.set_text(self._default)
                self.set_title(self._default)

            self.button = Gtk.Button(
                icon_name="user-trash-symbolic",
                can_focus=False,
            )
            self.button.add_css_class("transparent-button")

            self.add_suffix(self.button)

            self.button.connect("clicked", self.__onclick)
            self.connect("changed", self.__onchanged)

        def __onclick(self, *_):
            return self.parent.remove(self)

        def __onchanged(self, *_: "ColorExpanderRow.ColorEntryRow"):
            return self.set_title(self.get_text()[:8].lower())

        def __parse_title(self, color: str) -> str:
            color = "".join(
                char if char in set("0123456789abcdef") else "f"
                for char in color.lower()
            )
            return f"<b><span foreground='#{color:0<8}'>Color</span></b>"

        def set_title(self, title: str = "") -> None:
            return super().set_title(self.__parse_title(title))

        def get_text(self) -> str:
            return getattr(super(), "get_text", lambda: "")()

        def update_default(self):
            self._default = self.get_text()

    def __init__(self, title: str, subtitle: str, section: str):
        super().__init__()
        ToastOverlay.instances.append(self)
        self.section = section
        self.button_content = Adw.ButtonContent.new()
        self.button_content.set_icon_name("list-add-symbolic")
        self.button_content.set_label("Add Color")

        self.button = Gtk.Button.new()
        self.button.set_can_focus(False)
        self.button.set_child(self.button_content)
        self.button.add_css_class("transparent-button")

        self.set_title(title)
        self.set_subtitle(subtitle)
        self.add_row(self.button)
        self.button.connect(
            "clicked",
            lambda *_: self.add_row(ColorExpanderRow.ColorEntryRow(self, "777777FF")),
        )

        tmp = HyprData.get_option(self.section)

        if not tmp:
            tmp = Setting(self.section, 0)
            HyprData.new_option(tmp)

        if isinstance(tmp.value, (Gradient)):
            color: Color
            for color in tmp.value.colors:
                self.add_row(ColorExpanderRow.ColorEntryRow(self, color.rgba))

    def update_default(self) -> None:
        pass


class Adjustment(Gtk.Adjustment):
    def __init__(
        self,
        section: str,
        data_type: Type[Union[int, float]] = int,
        min: Union[int, float] = 0,
        max: Union[int, float] = 255,
    ):
        super().__init__()
        self.data_type = data_type
        self.set_lower(min)
        self.set_upper(max)
        self.set_page_size(0)

        if data_type.__name__ == "int":
            self.set_step_increment(1)
            self.set_page_increment(10)
        else:
            self.set_step_increment(0.1)
            self.set_page_increment(1.0)

        ToastOverlay.instances.append(self)
        self.section = section

        opt = HyprData.get_option(self.section)

        if not opt:
            opt = Setting(self.section, 1)
            HyprData.new_option(opt)

        if isinstance(opt.value, (int, float)):
            self.set_value(opt.value)

        self._default = (opt.value, False)
        self.connect("value-changed", self.__value_changed)

    def __value_changed(self, _):
        if self._default[0] != self.get_value():  # type: ignore
            if not self._default[1]:
                ToastOverlay.add_change()
                self._default = (self._default[0], True)
        else:
            ToastOverlay.del_change()
            self._default = (self._default[0], False)

        return HyprData.set_option(self.section, round(self.get_value()))

    def update_default(self) -> None:
        self._default = (self.get_value(), False)


class SpinRow:
    def __init__(
        self,
        title: str,
        subtitle: str,
        section: str,
        data_type: Type[Union[int, float]] = int,
        min: Union[int, float] = 0,
        max: Union[int, float] = 255,
        decimal_digits: int = 2,
    ):
        self._instance = Adw.SpinRow()
        self.instance.set_adjustment(Adjustment(section, data_type, min, max))
        self.instance.set_title(title)
        self.instance.set_subtitle(subtitle)

        if data_type.__name__ == "float":
            self.instance.set_digits(decimal_digits)

    @property
    def instance(self) -> Adw.SpinRow:
        return self._instance


class SwitchRow:
    def __init__(
        self, title: str, subtitle: str, section: str, *, invert: bool = False
    ) -> None:
        super().__init__()
        ToastOverlay.instances.append(self)
        self.__invert = invert
        self._instance = Adw.SwitchRow()
        self.instance.set_title(title)
        self.instance.set_subtitle(subtitle)
        self.section = section

        tmp = HyprData.get_option(self.section)

        if not tmp:
            tmp = Setting(self.section, False)
            HyprData.new_option(tmp)

        if self.__invert:
            self.instance.set_active(not tmp.value)
        else:
            self.instance.set_active(bool(tmp.value))

        self._default = self.instance.get_active()
        self.instance.connect("notify::active", self.__value_changed)

    def __value_changed(self, *_):
        if self.instance.get_active() != self._default:
            ToastOverlay.add_change()
        else:
            ToastOverlay.del_change()
        if self.__invert:
            return HyprData.set_option(self.section, not self.instance.get_active())
        return HyprData.set_option(self.section, self.instance.get_active())

    @property
    def instance(self) -> Adw.SwitchRow:
        return self._instance

    def update_default(self):
        self._default = self.instance.get_active()


class InfoButton(Gtk.MenuButton):
    def __init__(self, text: str) -> None:
        super().__init__(
            icon_name="help-info-symbolic",
        )
        self.set_icon_name("help-info-symbolic")
        self.set_sensitive(True)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.add_css_class("flat")
        self.set_popover()
        self.popover = Gtk.Popover.new()
        self.label = Gtk.Label.new(text)
        self.label.set_markup(text)
        self.label.set_wrap(True)
        self.label.set_max_width_chars(40)

        self.popover.set_child(self.label)
        self.set_popover(self.popover)


class ColorEntryRow(Adw.ActionRow):
    def __init__(self, title: str, description: str, section: str) -> None:
        super().__init__()
        ToastOverlay.instances.append(self)
        self.set_title(title)
        self.set_subtitle(description)
        self.entry = Gtk.Entry.new()
        self.add_suffix(self.entry)
        self.entry.set_valign(Gtk.Align.CENTER)

        self.section = section
        opt = HyprData.get_option(self.section)

        if not opt:
            opt = Setting(self.section, Color("00", "00", "00", "ff"))
            HyprData.new_option(opt)

        self.color: Color = opt.value  # type: ignore
        if isinstance(opt.value, (Color)):
            self.entry.set_text(opt.value.rgba)

        self._default = (self.get_text(), False)
        self.entry.connect("changed", self.__value_changed)

    def __value_changed(self, _):
        if self._default[0] != self.get_text():
            if not self._default[1]:
                ToastOverlay.add_change()
                self._default = (self._default[0], True)
        else:
            ToastOverlay.del_change()
            self._default = (self._default[0], False)

        txt = self.get_text()
        self.color.r = txt[0:2]
        self.color.g = txt[2:4]
        self.color.b = txt[4:6]
        self.color.a = txt[6:8]

        return HyprData.set_option(self.section, self.color)

    def update_default(self) -> None:
        self._default = (self.get_text(), False)

    def get_text(self) -> str:
        color: str = self.entry.get_text()[:8]  # type: ignore
        color = "".join(
            char if char in set("0123456789abcdef") else "f" for char in color.lower()
        )
        color = f"{color:0<8}"
        return color


class CheckButtonImage(Gtk.Box):
    def __init__(self, title: str, image: str) -> None:
        super().__init__()
        self.set_spacing(12)
        self.set_margin_top(6)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.checkbutton = Gtk.CheckButton.new_with_label(title)
        self.checkbutton.get_first_child().set_margin_start(12)  # type: ignore
        self.checkbutton.get_last_child().set_margin_start(6)  # type: ignore

        self.img = Gtk.Image.new_from_gicon(
            Gio.FileIcon.new(
                Gio.File.new_for_path("{}/icons/{}.svg".format(__file__[:-31], image))
            )
        )
        self.img.add_css_class("icon")
        self.img.set_pixel_size(200)

        self.img.set_hexpand(True)
        self.img.set_vexpand(True)

        self.img_container = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.img_container.add_css_class("background")
        self.img_container.add_css_class("frame")
        self.img_container.append(self.img)

        self.append(self.img_container)
        self.append(self.checkbutton)


class ButtonRow(Adw.ActionRow):
    def __init__(
        self, prefix: str, title: str, subtitle: str, onclick=lambda self: self
    ) -> None:
        super().__init__()
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.set_activatable(True)
        self.add_prefix(Icon(prefix))
        self.add_suffix(Icon("go-next-symbolic"))
        self.connect("activated", onclick)


class Icon(Gtk.Image):
    def __init__(
        self, name: str, size: Literal["large", "normal", "inherit"] = "normal"
    ) -> None:
        super().__init__()
        tmp_filepath = "{}/icons/{}.svg".format(__file__[:-31], name)
        if GLib.file_test(tmp_filepath, GLib.FileTest.EXISTS):
            self.set_from_gicon(Gio.FileIcon.new(Gio.File.new_for_path(tmp_filepath)))
        else:
            self.set_from_icon_name(name)

        match size:
            case "large":
                self.set_icon_size(Gtk.IconSize.LARGE)
            case "normal":
                self.set_icon_size(Gtk.IconSize.NORMAL)
            case "inherit":
                self.set_icon_size(Gtk.IconSize.INHERIT)
