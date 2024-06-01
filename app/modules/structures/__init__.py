import typing

import gi

gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk
from hyprparser import Color, Gradient, HyprData, Setting


class CustomToastOverlay:
    instances = []

    def __init__(self) -> None:
        self.changes = 0
        self._instance = Adw.ToastOverlay.new()
        self.toast = Adw.Toast.new("You have some unsaved changes!")
        self.toast.connect("button-clicked", self.save_changes)
        self.toast.set_button_label("Save now plz")
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
        if self.changes >= 1:
            self.show_toast()

    def del_change(self) -> None:
        self.changes -= 1
        if self.changes == 0:
            self.hide_toast()

    def save_changes(self, *_) -> None:
        if self.changes == 0:
            return

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

    def __onchanged(self, *_):
        return self.set_title(self.get_text()[:8].lower())

    def __parse_title(self, color: str) -> str:
        color = "".join(
            char if char in set("0123456789abcdef") else "f" for char in color
        )
        return f"<b><span foreground='#{color:f<8}'>Color</span></b>"

    def set_title(self, title: str = "") -> None:
        return super().set_title(self.__parse_title(title))

    def get_text(self) -> str:
        return getattr(super, "get_text", lambda: "")()

    def update_default(self):
        self._default = self.get_text()


class ColorExpanderRow(Adw.ExpanderRow):
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
        self.button.connect("clicked", lambda *_: self.add_row(ColorEntryRow(self, "")))

        tmp = HyprData.get_option(self.section)

        if not tmp:
            tmp = Setting(self.section, 0)
            HyprData.new_option(tmp)

        if isinstance(tmp.value, (Gradient)):
            color: Color
            for color in tmp.value.colors:
                self.add_row(ColorEntryRow(self, color.rgba))

    def update_default(self) -> None:
        pass


class Adjustment(Gtk.Adjustment):
    def __init__(self, section: str):
        super().__init__(
            value=0, lower=0, upper=1000, step_increment=1, page_increment=10
        )
        ToastOverlay.instances.append(self)
        self.section = section

        opt = HyprData.get_option(self.section)

        if not opt:
            opt = Setting(self.section, 0)
            HyprData.new_option(opt)

        if isinstance(opt.value, (int, float)):
            self.set_value(opt.value)

        self._default = (opt.value, False)
        self.connect("value-changed", self.__value_changed)

    def __value_changed(self, _):
        if self._default[0] != round(self.get_value()):
            if not self._default[1]:
                ToastOverlay.add_change()
                self._default = (self._default[0], True)
        else:
            ToastOverlay.del_change()
            self._default = (self._default[0], False)

        return HyprData.set_option(self.section, round(self.get_value()))

    def update_default(self) -> None:
        self._default = (round(self.get_value()), False)


class SpinRow:
    def __init__(self, title: str, subtitle: str, section: str):
        self._instance = Adw.SpinRow()
        self.instance.set_adjustment(Adjustment(section))
        self.instance.set_title(title)
        self.instance.set_subtitle(subtitle)

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
