from .CustomToastOverlay import ToastOverlay
from ..imports import Adw, Gtk, HyprData, Setting, Color
from ..utils import ParseColor


class ColorEntryRow(Adw.ActionRow):
    def __init__(self, title: str, description: str, section: str) -> None:
        super().__init__()

        ToastOverlay.instances.append(self)

        self.set_title(title)
        self.set_subtitle(description)

        self.entry = Gtk.Entry.new()
        self.stack = Gtk.Stack.new()
        self.button_showcolor = Gtk.ToggleButton.new()
        self.colorbutton = Gtk.ColorButton.new()
        self.colorbutton.set_use_alpha(True)
        self.gdkcolor = self.colorbutton.get_rgba()   # type:ignore

        self.add_suffix(self.stack)
        self.add_suffix(self.button_showcolor)

        self.button_showcolor.set_icon_name('document-edit-symbolic')
        self.button_showcolor.add_css_class('flat')
        self.button_showcolor.set_valign(Gtk.Align.CENTER)

        self.entry.set_valign(Gtk.Align.CENTER)
        self.colorbutton.set_valign(Gtk.Align.CENTER)

        self.stack.set_hhomogeneous(False)
        self.stack.set_interpolate_size(True)
        self.stack.add_named(self.colorbutton, 'color-button')
        self.stack.add_named(self.entry, 'entry')
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        self.section = section
        opt = HyprData.get_option(self.section)

        if not opt:
            opt = Setting(self.section, Color('00', '00', '00', '00'))
            HyprData.new_option(opt)

        if isinstance(opt.value, (Color)):
            self.color: Color = opt.value

            self.entry.set_text('#' + self.color.hex)
            self.gdkcolor = ParseColor.hex_to_gdk_rgba(self.color.hex)
            self.colorbutton.set_rgba(self.gdkcolor)   # type: ignore

        self._default = (self.entry.get_text(), False)   # type: ignore
        self.entry.connect('changed', self.on_changed)
        self.colorbutton.connect('color-set', self.on_color_set)
        self.button_showcolor.connect('toggled', self.on_toggled)

    def on_toggled(self, _: Gtk.ToggleButton) -> None:
        if self.button_showcolor.get_active():
            return self.stack.set_visible_child_name('entry')
        return self.stack.set_visible_child_name('color-button')

    def on_changed(self, _: Gtk.Entry) -> None:

        if not self.gdkcolor.parse(self.entry.get_text()):   # type: ignore
            return

        self.colorbutton.set_rgba(self.gdkcolor)   # type: ignore

        color = ParseColor.gdk_rgba_to_hex(self.gdkcolor).removeprefix('#')
        self.color.r = color[0:2]
        self.color.g = color[2:4]
        self.color.b = color[4:6]
        self.color.a = color[6:8]

        HyprData.set_option(self.section, self.color)

        return self.add_change()

    def on_color_set(self, _: Gtk.ColorButton) -> None:

        color = ParseColor.gdk_rgba_to_hex(self.gdkcolor).removeprefix('#')

        self.color.r = color[0:2]
        self.color.g = color[2:4]
        self.color.b = color[4:6]
        self.color.a = color[6:8]

        self.entry.set_text(ParseColor.gdk_rgba_to_hex(self.gdkcolor))

        HyprData.set_option(self.section, self.color)

        return self.add_change()

    def add_change(self) -> None:
        if self._default[0] != self.entry.get_text():   # type: ignore
            if not self._default[1]:
                ToastOverlay.add_change()
                self._default = (self._default[0], True)
        else:
            ToastOverlay.del_change()
            self._default = (self._default[0], False)
        return

    def update_default(self) -> None:
        self._default = (self.entry.get_text(), False)   # type: ignore
