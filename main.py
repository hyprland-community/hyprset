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
        super().__init__(title="Hello World")
        self.list = Gtk.ListBox()
        self.add(self.list)
        
        conf = get_conf()
        print(conf)
        sections = inspect.getmembers(conf, lambda a:not(inspect.isroutine(a)))
        sections = [a for a in sections if not(a[0].startswith('__') and a[0].endswith('__'))]
        for section in sections:
            options = inspect.getmembers(section[1], lambda a:not(inspect.isroutine(a)))
            options = [a for a in options if not(a[0].startswith('__') and a[0].endswith('__'))]
            for setting,value in options:
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
                box.pack_start(Gtk.Label(setting), True, True, 0)
                box.pack_start(Gtk.Button(label=str(value)), True, True, 0)
                self.list.insert(box, -1)

    def on_button_clicked(self, widget):
        print("Hello World")


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()