# ruff: noqa
from typing import List, Literal, Type, Union, Tuple, Optional


import gi
import re
import string

gi.require_versions({"Adw": "1", "GdkPixbuf": "2.0", "Gdk": "4.0", "Gtk": "4.0"})
from gi.repository import Adw, Gdk, GdkPixbuf, Gio, GLib, Gtk, cairo, GObject
from hyprparser import Bezier, Color, Gradient, HyprData, Setting

Gtk.Settings.get_default().set_property("gtk-icon-theme-name", "Adwaita")  # type: ignore

# Gtk.IconTheme.get_for_display(Gdk.Display.get_default()).add_search_path(
#     __file__[:-19] + "/icons"
# )
