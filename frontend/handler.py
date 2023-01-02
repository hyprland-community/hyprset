from gi.repository import Gtk

class SignalHandler():

    def __init__(self, app):
        self.app = app

    def on_main_window_destroy(self, *args):
        Gtk.main_quit(*args)

    def test(self, *args, **kwargs):
        print(args)
        print(kwargs)