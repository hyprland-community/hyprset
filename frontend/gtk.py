import gi
import hyprland
import asyncio

from .handler import SignalHandler
import consts

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Hyprset_glade(Gtk.Application):
    def __init__(self,b):
        self.pages = {}
        self.backend = b
        self.handler = SignalHandler(self)
        super().__init__(application_id=consts.APP_ID)
        self.builder = Gtk.Builder.new_from_file(consts.UI_HYPRSET)
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
    
    def create_card(self,setting,value,doc):
        card = Gtk.Box()
        card.set_orientation(Gtk.Orientation.HORIZONTAL)
        card.set_halign(Gtk.Align.FILL)
        card.set_homogeneous(True)
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
            case bool():
                entry = Gtk.Switch()
                entry.set_active(value)
            case int():
                entry = Gtk.Entry() 
                entry.set_text(str(value))
            case float():
                entry = Gtk.Entry()
                entry.set_text(str(value))
            case _:
                entry = Gtk.Label("Unknown type")
        entry.set_halign(Gtk.Align.END)
        card.add(entry)
        card.set_tooltip_text(doc)
        return card

    def do_activate(self):
        self.main_window.present()


def show(backend):
    Hyprset_glade(backend).run()
    Gtk.main()