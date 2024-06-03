# ruff: noqa
from typing import List, Union

import gi

gi.require_version("Adw", "1")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Adw, Gdk, GdkPixbuf, Gio, GLib, Gtk
from hyprparser import Color, Gradient, HyprData, Setting
