import hyprland
import inspect
import asyncio


class Backend:
    def get_conf(self):
        self.conf = asyncio.run(hyprland.Config.from_conf())
        return self.conf

    def make_tabs(self):
        conf = self.get_conf()
        tabs = {}
        for section in hyprland.Config.get_sections():
            options = inspect.getmembers(getattr(conf, section), lambda a:not(inspect.isroutine(a)))
            options = [a for a in options if not(a[0].startswith('__') and a[0].endswith('__'))]
            tabs[section] = []
            
            for setting,value in options:
                # more parsing here once done, color and beziers and stuff
                doc = getattr(getattr(conf,section), f'set_{setting}').__doc__
                tabs[section].append((setting, value, doc))
        return tabs
    
    def update_conf(self,section,setting,value):
        setattr(getattr(self.conf,section),setting.replace('.','__'),value)