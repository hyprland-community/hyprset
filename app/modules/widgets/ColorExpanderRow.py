from gi.repository import Gdk
from ..imports import Adw, Gtk, HyprData, Gradient, Color, Setting
from ..utils import ParseColor
from .CustomToastOverlay import ToastOverlay


class ColorExpanderRow(Adw.ExpanderRow):
    class ColorEntryRow(Adw.EntryRow):
        def __init__(self, parent: 'ColorExpanderRow', new_color: str = ''):
            super().__init__()
            self.parent = parent
            self.set_title('Color')
            self.gdkcolor = Gdk.RGBA(0, 0, 0, 1)   # type:ignore
            ToastOverlay.instances.append(self)

            if new_color:
                self._default = new_color
                self.set_text(self._default)
                self.set_title('Color')
                self.on_changed(self)

            self.button = Gtk.Button.new()

            self.button.set_icon_name('user-trash-symbolic')
            self.button.set_can_focus(False)
            self.button.add_css_class('flat')
            self.button.set_valign(Gtk.Align.CENTER)

            self.add_suffix(self.button)

            self.button.connect('clicked', self.on_clicked)
            self.connect('changed', self.on_changed)

        def on_clicked(self, *_: Gtk.Button):
            return self.parent.remove(self)

        def on_changed(self, *_: 'ColorExpanderRow.ColorEntryRow'):
            if self.gdkcolor.parse(self.get_text()):
                self._default = ParseColor.gdk_rgba_to_hex(self.gdkcolor)
                return self.set_title(
                    f'<b><span foreground="{self._default}"> Color </span></b>'
                )
            return self.set_title(
                f'<b><span foreground="{self._default}"> Color </span></b>'
            )

        def get_text(self) -> str:
            return getattr(super(), 'get_text', lambda: '')()

        def update_default(self):
            self._default = ParseColor.gdk_rgba_to_hex(self.gdkcolor)

    def __init__(self, title: str, subtitle: str, section: str):
        super().__init__()
        ToastOverlay.instances.append(self)
        self.section = section

        self.button = Adw.ActionRow.new()
        self.button.set_activatable(True)
        self.button.set_icon_name('list-add-symbolic')
        self.button.set_title('Add Color')
        self.button.set_hexpand(True)
        self.button.get_child().set_halign(Gtk.Align.CENTER)

        self.set_title(title)
        self.set_subtitle(subtitle)
        self.add_row(self.button)
        self.button.connect(
            'activated',
            lambda *_: self.add_row(
                ColorExpanderRow.ColorEntryRow(self, '#777777FF')
            ),
        )

        opt = HyprData.get_option(self.section)

        if not opt:
            opt = Setting(self.section, 0)
            HyprData.new_option(opt)

        if isinstance(opt.value, (Gradient)):
            color: Color
            for color in opt.value.colors:
                self.add_row(
                    ColorExpanderRow.ColorEntryRow(self, '#' + color.hex)
                )

    def update_default(self) -> None:
        pass
