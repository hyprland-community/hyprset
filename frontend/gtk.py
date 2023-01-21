import gi
import hyprland
import asyncio

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .handler import SignalHandler
from . import consts

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
                page.add(self.create_card(*setting,tab=tab))
            scrolled.add(page)
            self.pages[tab] = scrolled
            self.tab_bar.append_page(scrolled, Gtk.Label(tab))
    
    def create_card(self,setting,value,doc,tab=None):
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
                setattr(entry,"__setting",setting)
                setattr(entry,"__section",tab)
                entry.connect("changed",self.handler.callback_entry)
                entry.set_text(str(value))
            case bool():
                entry = Gtk.Switch()
                entry.set_halign(Gtk.Align.END)
                setattr(entry,"__setting",setting)
                setattr(entry,"__section",tab)
                entry.connect("state-set",self.handler.callback_switch)
                entry.set_active(value)
            case int():
                entry = Gtk.Scale() 
                setattr(entry,"__setting",setting)
                setattr(entry,"__section",tab)
                entry.set_range(0,100)
                entry.set_value(value)
                entry.set_digits(0)
                entry.set_increments(1,10)

                entry.connect("value-changed",self.handler.callback_scale)
            case float():
                entry = Gtk.Scale() 
                setattr(entry,"__setting",setting)
                setattr(entry,"__section",tab)
                entry.set_range(0,10)
                entry.set_value(value)
                entry.set_digits(2)
                entry.set_increments(0.1,1)

                entry.connect("value-changed",self.handler.callback_scale)
            case _:
                entry = Gtk.Label("Unknown type")
        
        card.add(entry)
        card.set_tooltip_text(doc)
        return card

    def do_activate(self):
        self.main_window.present()


def show(backend):
    Hyprset_glade(backend).run()
    Gtk.main()