from gi.repository import Gtk

class SignalHandler():

    def __init__(self, app):
        self.app = app

    def on_main_window_destroy(self, *args):
        Gtk.main_quit(*args)

    def test(self, *args, **kwargs):
        print(args)
        print(kwargs)
    
    def callback_scale(self,widget):
        section = getattr(widget,"__section")
        setting = getattr(widget,"__setting")
        value = widget.get_value()
        print(section,setting,value)
        self.app.backend.update_conf(section,setting,value)

    def callback_entry(self,widget):
        section = getattr(widget,"__section")
        setting = getattr(widget,"__setting")
        value = widget.get_text()
        print(section,setting,value)
        self.app.backend.update_conf(section,setting,value)
    
    def callback_switch(self,widget,value):
        section = getattr(widget,"__section")
        setting = getattr(widget,"__setting")
        print(section,setting,value)
        self.app.backend.update_conf(section,setting,value)