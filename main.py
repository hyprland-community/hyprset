import gi
import hyprland
import asyncio
import inspect

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def get_conf():
    return asyncio.run(hyprland.Config.from_conf())

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hyprset")
        self.tabs = {}

        self.main_box = Gtk.ScrolledWindow()
        self.main_box.add(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6))
        
        conf = get_conf()
        print(conf)

        sections = inspect.getmembers(conf, lambda a:not(inspect.isroutine(a)))
        sections = [a for a in sections if not(a[0].startswith('__') and a[0].endswith('__'))]
        for section in hyprland.Config.get_sections():
            options = inspect.getmembers(getattr(conf, section), lambda a:not(inspect.isroutine(a)))
            options = [a for a in options if not(a[0].startswith('__') and a[0].endswith('__'))]
            self.tabs[section] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            for setting,value in options:
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                box.add(Gtk.Label(label=setting))
                box.add(Gtk.Button(label=str(value)))
                self.tabs[section].add(box)
        
        header = Gtk.HeaderBar()
        header.set_show_close_button(False)
        for tab in self.tabs:
            button = Gtk.Button(label=tab)
            button.connect("clicked", self.on_button_clicked)
            header.add(button)
        self.set_titlebar(header)
        self.add(self.main_box)


    def new_list():
        l = Gtk.ListBox()
        scroll = Gtk.ScrolledWindow()
        scroll.add(l)
        return scroll

    def on_button_clicked(self, widget):
        if self.main_box.get_children():
            self.main_box.remove(self.main_box.get_children()[0])
        self.main_box.add(self.tabs[widget.get_label()])
        
        self.show_all()


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
print("beep boop")
Gtk.main()