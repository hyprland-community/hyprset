import gi
import hyprland
import asyncio
import inspect

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

TITLE = "Hyprset"
DEFAULT_TAB = "general"

def get_conf():
    return asyncio.run(hyprland.Config.from_conf())

class Hyprset(Gtk.Window):
    def __init__(self):
        super().__init__(title=TITLE)

        self.tabs = self.make_tabs()
        self.main_box = Gtk.ScrolledWindow()
        #self.main_box.add(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6))

        self.main_box.add(self.tabs[DEFAULT_TAB])

        header = Gtk.HeaderBar()
        header.set_show_close_button(False)
        for tab in self.tabs:
            button = Gtk.Button(label=tab)
            button.connect("clicked", self.on_button_clicked)
            header.add(button)
        self.set_titlebar(header)
        self.add(self.main_box)

    def make_tabs(self):
        conf = get_conf()
        tabs = {}
        for section in hyprland.Config.get_sections():
            options = inspect.getmembers(getattr(conf, section), lambda a:not(inspect.isroutine(a)))
            options = [a for a in options if not(a[0].startswith('__') and a[0].endswith('__'))]
            tabs[section] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            for setting,value in options:
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                box.add(Gtk.Label(label=setting))
                if type(value) == bool:
                    switch = Gtk.Switch()
                    switch.set_active(value)
                    box.add(switch)
                else:
                    box.add(Gtk.Button(label=str(value)))
                tabs[section].add(box)
        return tabs

    def on_button_clicked(self, widget):
        if self.main_box.get_children():
            self.main_box.remove(self.main_box.get_children()[0])
        self.main_box.add(self.tabs[widget.get_label()])
        
        self.show_all()


win = Hyprset()
win.connect("destroy", Gtk.main_quit)
win.show_all()
print("beep boop")
Gtk.main()