import hyprland
import inspect
import asyncio


class Backend:
    def get_conf(self):
        return asyncio.run(hyprland.Config.from_conf())

    def make_tabs(self):
        conf = self.get_conf()
        tabs = {}
        for section in hyprland.Config.get_sections():
            options = inspect.getmembers(getattr(conf, section), lambda a:not(inspect.isroutine(a)))
            options = [a for a in options if not(a[0].startswith('__') and a[0].endswith('__'))]
            tabs[section] = []
            for setting,value in options:
                tabs[section].append((setting, value))
        return tabs
