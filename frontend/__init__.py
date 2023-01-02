import gi
import hyprland
import asyncio
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

TITLE = "Hyprset"
DEFAULT_TAB = "general"

def get_conf():
    return asyncio.run(hyprland.Config.from_conf())

class SignalHandler():
    def __init__(self, app):
        self.app = app

    def on_main_window_destroy(self, *args):
        Gtk.main_quit(*args)

    def test(self, *args, **kwargs):
        print(args)
        print(kwargs)

class Hyprset_glade(Gtk.Application):
    def __init__(self,b):
        self.pages = {}
        self.backend = b
        self.handler = SignalHandler(self)
        super().__init__(application_id="com.flicko.test")
        self.builder = Gtk.Builder.new_from_file('ui/hyprset.glade')
        self.main_window = self.builder.get_object("main_window")
        self.tab_bar = self.builder.get_object("tab_bar")
        self.builder.connect_signals(self.handler)
        self.populate_tabs()
        
        self.main_window.show_all()
    
    def populate_tabs(self):
        self.tabs = self.backend.make_tabs()
        for tab,settings in self.tabs.items():
            scrolled = Gtk.ScrolledWindow()
            page = Gtk.Box()
            page.set_orientation(Gtk.Orientation.VERTICAL)
            for setting in settings:
                page.add(self.create_card(*setting))
            scrolled.add(page)
            self.pages[tab] = scrolled
            self.tab_bar.append_page(scrolled, Gtk.Label(tab))
    
    def create_card(self,setting,value):
        card = Gtk.Box()
        card.set_orientation(Gtk.Orientation.HORIZONTAL)
        card.set_margin_top(10)
        card.set_margin_bottom(10)
        card.set_margin_start(10)
        card.set_margin_end(10)
        card.set_spacing(10)
        label = Gtk.Label(setting)
        label.set_halign(Gtk.Align.START)
        card.add(label)
        match value:
            case str():
                entry = Gtk.Entry() 
                entry.set_text(str(value))
            case int():
                entry = Gtk.SpinButton()
                entry.set_range(0,100)
                entry.set_value(value)
            case bool():
                entry = Gtk.Switch()
                entry.set_active(value)
            case _:
                entry = Gtk.Label("Unknown type")
        entry.set_halign(Gtk.Align.END)
        card.add(entry)
        return card


    
    def on_tabchange(self, *args, **kwargs):
        print(args)
        print(kwargs)


    def do_activate(self):
        self.main_window.present()


def show(b):
    Hyprset_glade(b).run()
    Gtk.main()