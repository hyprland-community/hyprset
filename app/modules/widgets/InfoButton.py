from ..imports import Gtk


class InfoButton(Gtk.MenuButton):
    def __init__(self, text: str) -> None:
        super().__init__(
            icon_name='help-info-symbolic',
        )
        self.set_icon_name('help-info-symbolic')
        self.set_sensitive(True)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.add_css_class('flat')
        self.set_popover()
        self.popover = Gtk.Popover.new()
        self.label = Gtk.Label.new(text)
        self.label.set_markup(text)
        self.label.set_wrap(True)
        self.label.set_max_width_chars(40)

        self.popover.set_child(self.label)
        self.set_popover(self.popover)
