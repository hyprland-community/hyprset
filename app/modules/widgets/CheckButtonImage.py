from ..imports import Gtk
from .Icon import Icon


class CheckButtonImage(Gtk.Box):
    def __init__(self, title: str, image: str) -> None:
        super().__init__()
        self.set_spacing(12)
        self.set_margin_top(6)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.checkbutton = Gtk.CheckButton.new_with_label(title)
        self.checkbutton.get_first_child().set_margin_start(12)
        self.checkbutton.get_last_child().set_margin_start(6)

        self.img = Icon(image)
        self.img.add_css_class('icon')
        self.img.set_pixel_size(200)

        self.img.set_hexpand(True)
        self.img.set_vexpand(True)

        self.img_container = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.img_container.add_css_class('background')
        self.img_container.add_css_class('frame')
        self.img_container.append(self.img)

        self.append(self.img_container)
        self.append(self.checkbutton)
