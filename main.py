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

                infobox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                infobox.add(Gtk.Label(label=setting,halign=Gtk.Align.START))
                infobox.add(Gtk.Label(label=getattr(getattr(conf, section),f'set_{setting}').__doc__,halign=Gtk.Align.START))

                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                box.add(infobox)
                if type(value) is bool:
                    switch = Gtk.Switch(halign=Gtk.Align.END)
                    switch.set_active(value)
                    box.add(switch)
                elif type(value) is int:
                    spin = Gtk.SpinButton(halign=Gtk.Align.END)
                    spin.set_range(0, 255)
                    spin.set_increments(1, 1)
                    spin.set_value(value)
                    box.add(spin)
                elif type(value) is str:
                    entry = Gtk.Entry(halign=Gtk.Align.END)
                    entry.set_text(value)
                    box.add(entry)   
                else:
                    box.add(Gtk.Button(label=str(value),halign=Gtk.Align.END))
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